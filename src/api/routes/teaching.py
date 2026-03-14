"""Teaching: POST /teach, POST /correct."""

from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas import TeachRequest, TeachResponse, CorrectRequest
from src.api.deps import DbSession, CurrentUser
from src.api.session_helpers import get_or_create_teaching_session
from src.api.domain_helpers import get_domain_adapter, get_tracker_for_ta, save_tracker_to_ta
from src.db.models import TAInstance, TeachingEvent
from src.core.teaching_events import make_teaching_event
from src.core.teaching_interpreter import interpret_teaching
from src.core.orchestrator import run_teaching_and_test, run_correction
from src.core.trace import set_trace_db_session

router = APIRouter(tags=["teaching"])


def _get_ta(ta_id: int, user_id: int, db: DbSession) -> TAInstance:
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == user_id,
    ).first()
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    return ta


@router.post("/api/ta/{ta_id}/teach", response_model=TeachResponse)
def teach(
    ta_id: int,
    body: TeachRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    ta = _get_ta(ta_id, current_user.id, db)
    session = get_or_create_teaching_session(db, ta.id)
    set_trace_db_session(db, session.id)
    tracker = get_tracker_for_ta(ta)
    adapter = get_domain_adapter(ta.domain_id)
    unit_ids = [u["id"] for u in adapter.load_knowledge_units()]

    # Interpret student input -> teaching event
    filled_prompt = adapter.get_teaching_interpreter_prompt(body.student_input)
    interpreted = interpret_teaching(
        body.student_input,
        unit_ids,
        filled_prompt=filled_prompt,
        use_llm=True if filled_prompt else None,
    )
    topic = interpreted.get("topic_taught", "Teaching")
    units_taught = interpreted.get("knowledge_units_taught", [])
    quality = interpreted.get("quality_score", 0.6)
    if not units_taught:
        units_taught = [unit_ids[0]] if unit_ids else []

    teaching_event = make_teaching_event(topic, units_taught, note=body.student_input[:500])

    conversation_history = []
    for te in db.query(TeachingEvent).filter(TeachingEvent.session_id == session.id).order_by(TeachingEvent.created_at.asc()).all():
        if te.student_input:
            conversation_history.append({"role": "student", "content": te.student_input})
        if te.ta_response:
            conversation_history.append({"role": "ta", "content": te.ta_response})

    result = run_teaching_and_test(
        tracker,
        adapter.load_problems(),
        teaching_event,
        run_attempt=True,
        domain_adapter=adapter,
        conversation_history=conversation_history,
    )
    learned = result["learned_units"]
    ta_response = result["ta_learner_response"]

    save_tracker_to_ta(ta, tracker, db)

    te = TeachingEvent(
        session_id=session.id,
        teaching_event_id=teaching_event["teaching_event_id"],
        student_input=body.student_input[:2000] if body.student_input else None,
        topic_taught=topic,
        interpreted_units=units_taught,
        quality_score=quality,
        ta_response=ta_response[:2000] if ta_response else None,
    )
    db.add(te)
    db.commit()

    return TeachResponse(
        teaching_event_id=teaching_event["teaching_event_id"],
        interpreted_units=units_taught,
        topic_taught=topic,
        quality_score=quality,
        state_update={"learned": sorted(learned)},
        ta_response=ta_response,
    )


@router.post("/api/ta/{ta_id}/correct")
def correct(
    ta_id: int,
    body: CorrectRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    ta = _get_ta(ta_id, current_user.id, db)
    tracker = get_tracker_for_ta(ta)
    applied, _ = run_correction(
        tracker,
        unit_id=body.unit_id,
        misconception_id=body.misconception_id,
        trigger="explicit_correction_event",
    )
    save_tracker_to_ta(ta, tracker, db)
    return {"correction_applied": applied, "new_state": tracker.get_state()}
