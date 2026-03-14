"""Teaching: POST /teach, POST /correct."""

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas import TeachRequest, TeachResponse, CorrectRequest
from src.api.deps import DbSession, CurrentUser
from src.api.session_helpers import get_or_create_teaching_session
from src.db.models import TAInstance, TeachingEvent
from src.core.knowledge_state import StateTracker
from src.core.teaching_events import make_teaching_event, apply_teaching_event
from src.core.teaching_interpreter import interpret_teaching
from src.core.dialogue_engine import get_ta_learner_response
from src.core.trace import (
    set_trace_db_session,
    record_teaching_event,
    record_knowledge_state_update,
    record_learner_dialogue,
)
from src.core.misconception_engine import apply_correction
from src.domains.python_domain import PythonDomainAdapter

router = APIRouter(tags=["teaching"])

_SEED_DIR = Path(__file__).resolve().parent.parent.parent.parent / "seed"


def _get_ta(ta_id: int, user_id: int, db: DbSession) -> TAInstance:
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == user_id,
    ).first()
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    return ta


def _tracker_from_ta(ta: TAInstance) -> StateTracker:
    adapter = PythonDomainAdapter(seed_dir=_SEED_DIR)
    units = adapter.load_knowledge_units()
    tracker = StateTracker(unit_definitions=units, domain=ta.domain_id)
    if ta.knowledge_state and "units" in ta.knowledge_state:
        for uid, rec in ta.knowledge_state["units"].items():
            if uid in tracker._state:
                tracker._state[uid] = dict(rec)
    return tracker


def _save_tracker_to_ta(ta: TAInstance, tracker: StateTracker, db: DbSession):
    ta.knowledge_state = tracker.get_full_state()
    db.add(ta)
    db.commit()


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
    tracker = _tracker_from_ta(ta)
    adapter = PythonDomainAdapter(seed_dir=_SEED_DIR)
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

    # State update
    record_teaching_event(
        domain=tracker.get_domain(),
        topic_taught=topic,
        knowledge_units_taught=units_taught,
        note=body.student_input[:500],
        teaching_event_id=teaching_event["teaching_event_id"],
    )
    state_before = {u: tracker.get_state().get(u, "unknown") for u in units_taught}
    apply_teaching_event(tracker, teaching_event)
    record_knowledge_state_update(
        domain=tracker.get_domain(),
        trigger=teaching_event["teaching_event_id"],
        unit_ids=units_taught,
        state_before=state_before,
        state_after={u: "learned" for u in units_taught},
        evidence_source=teaching_event["teaching_event_id"],
    )

    # TA response
    learned = tracker.get_learned_units()
    active_mis = tracker.get_active_misconception_ids(learned)
    filled = adapter.get_conversation_prompt(
        tracker.get_full_state(), teaching_event, list(learned)
    )
    ta_response = get_ta_learner_response(
        learned, teaching_event, active_misconceptions=active_mis or None,
        filled_prompt=filled, use_llm=True if filled else None,
    )
    record_learner_dialogue(
        domain=tracker.get_domain(),
        teaching_event_id=teaching_event["teaching_event_id"],
        learned_unit_ids=sorted(learned),
        response_text=ta_response,
        active_misconception_ids=active_mis,
    )

    _save_tracker_to_ta(ta, tracker, db)

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
    tracker = _tracker_from_ta(ta)
    applied = apply_correction(
        tracker,
        unit_id=body.unit_id,
        misconception_id=body.misconception_id,
        trigger="explicit_correction_event",
    )
    _save_tracker_to_ta(ta, tracker, db)
    return {"correction_applied": applied, "new_state": tracker.get_state()}
