"""Teaching: POST /teach, POST /correct, POST /analyze-teaching, POST /teach/stream (SSE)."""

import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.api.schemas import TeachRequest, TeachResponse, CorrectRequest
from src.api.deps import DbSession, CurrentUser
from src.api.session_helpers import get_or_create_teaching_session
from src.api.domain_helpers import get_domain_adapter, get_tracker_for_ta, save_tracker_to_ta
from src.db.models import TAInstance, TeachingEvent
from src.core.teaching_events import make_teaching_event
from src.core.teaching_interpreter import interpret_teaching
from src.core.orchestrator import run_teaching_and_test, run_correction
from src.core.trace import set_trace_db_session
from src.core.teaching_helper import analyze_teaching
from src.core.reflect_respond import (
    extract_new_knowledge,
    update_reflection_store,
    retrieve_relevant,
    generate_constrained_response_stream,
)
from src.core.teaching_events import apply_teaching_event
from src.core.mode_shifting import maybe_append_questioner_response
from src.core.bug_evaluator import evaluate_bug_identification, get_progressive_hint, compute_hint_level
from src.core.chat_behavior import analyze_message_for_cheating

router = APIRouter(tags=["teaching"])


def _teach_stream_generator(
    tracker,
    ta,
    session,
    db,
    teaching_event: dict,
    adapter,
    conversation_history: list,
    learned: list,
    active_mis_ids: list,
    problem_id: str | None = None,
):
    """Yield SSE events: chunk (text) then done (full response + metadata). Saves state after done."""
    from src.core.reflect_respond import _last_n_messages
    store = tracker.get_reflection_store()
    topic = teaching_event.get("topic_taught", "")
    note = teaching_event.get("note", "")
    prompt_rules = adapter.get_conversation_prompt(
        tracker.get_full_state(),
        teaching_event,
        learned,
    )

    current_problem = None
    if problem_id:
        problems = adapter.load_problems()
        current_problem = next((p for p in problems if p.get("problem_id") == problem_id), None)
        if current_problem and current_problem.get("problem_type") == "buggy-code":
            guided = adapter.get_guided_teaching_prompt(
                current_problem.get("problem_type", ""),
                current_problem.get("problem_statement", ""),
            )
            if guided:
                prompt_rules = f"{prompt_rules}\n\n{guided}" if prompt_rules else guided

    messages = _last_n_messages(conversation_history or [], note, n=5)
    extracted = extract_new_knowledge(messages, tracker.get_domain())
    updated_store = update_reflection_store(store, extracted)
    retrieved = retrieve_relevant(
        updated_store, topic, note, tracker.get_domain(),
        learned_unit_ids=learned, active_misconceptions=active_mis_ids,
    )

    code_modification = None
    bug_eval_result = None

    # M-83: Check if clarification is needed (low confidence teaching)
    needs_clarification = teaching_event.get("needs_clarification", False)
    confidence = teaching_event.get("confidence", 0.5)

    # M-81: Thinking process visualization
    thinking_text = "🤔 TA is thinking..."
    if needs_clarification:
        thinking_text = "🤔 TA is confused and needs clarification..."
    yield f"data: {json.dumps({'type': 'thinking', 'text': thinking_text})}\n\n"

    # M-83: If confidence is too low, request clarification instead of normal response
    if needs_clarification and confidence < 0.35:
        clarifying_questions = [
            "I'm not quite sure I understood that. Could you explain it in a different way?",
            "I'm a bit confused about what you just taught. Can you give me a concrete example?",
            "I want to make sure I understand correctly. Could you break that down into smaller steps?",
        ]
        import random
        clarification = random.choice(clarifying_questions)
        yield f"data: {json.dumps({'type': 'chunk', 'text': clarification})}\n\n"
        yield f"data: {json.dumps({'type': 'done', 'ta_response': clarification, 'interpreted_units': [], 'topic_taught': topic, 'code_modification': None, 'needs_clarification': True})}\n\n"
        return  # Skip normal Reflect-Respond pipeline

    full_parts: list[str] = []
    thinking_parts: list[str] = []
    is_thinking = False

    quality_score = teaching_event.get("quality_score")

    for chunk in generate_constrained_response_stream(
        retrieved, topic, note, learned, active_mis_ids, tracker.get_domain(),
        conversation_history=conversation_history, ask_why_or_how=True, prompt_rules=prompt_rules,
        quality_score=quality_score,
    ):
        # Handle thinking markers
        if chunk.startswith("[THINKING]"):
            is_thinking = True
            thinking_content = chunk.replace("[THINKING]", "").replace("[/THINKING]", "")
            thinking_parts.append(thinking_content)
            yield f"data: {json.dumps({'type': 'thinking', 'text': thinking_content})}\n\n"
            continue
        if "[/THINKING]" in chunk:
            is_thinking = False
            continue

        full_parts.append(chunk)
        yield f"data: {json.dumps({'type': 'chunk', 'text': chunk})}\n\n"

    ta_response = "".join(full_parts).strip()
    # Dynamic length handling - no longer hard-coding 400
    msg_count = (len(conversation_history) + 1) if conversation_history else 1
    ta_response = maybe_append_questioner_response(
        ta_response, msg_count, topic, note, tracker.get_domain(),
        list(learned), active_mis_ids, conversation_history, phase="teach",
    )

    # Evaluate bug identification after streaming (does not block first chunk)
    if current_problem and current_problem.get("problem_type") == "buggy-code":
        try:
            bug_eval_result = evaluate_bug_identification(
                note, current_problem, conversation_history,
            )
            code_modification = bug_eval_result.get("code_modification")
        except Exception:
            pass

    # Append hint if bug evaluation failed and student needs help
    if bug_eval_result and not bug_eval_result.get("correct") and current_problem:
        incorrect_count = _count_incorrect_attempts(conversation_history, problem_id or "")
        hint_level = compute_hint_level(incorrect_count)
        if hint_level > 0:
            hint = get_progressive_hint(current_problem, hint_level, conversation_history)
            if hint:
                ta_response += f"\n\n💡 Hint: {hint}"

    tracker.set_reflection_store(updated_store)
    yield f"data: {json.dumps({'type': 'done', 'ta_response': ta_response, 'interpreted_units': teaching_event.get('knowledge_units_taught', []), 'topic_taught': topic, 'code_modification': code_modification})}\n\n"
    save_tracker_to_ta(ta, tracker, db)
    te = TeachingEvent(
        session_id=session.id,
        teaching_event_id=teaching_event["teaching_event_id"],
        student_input=teaching_event.get("note", "")[:2000],
        topic_taught=topic,
        interpreted_units=teaching_event.get("knowledge_units_taught", []),
        quality_score=teaching_event.get("quality_score", 0.6),
        ta_response=ta_response[:2000] if ta_response else None,
    )
    db.add(te)
    db.commit()


def _count_incorrect_attempts(conversation_history: list[dict] | None, problem_id: str) -> int:
    """Estimate incorrect attempts based on conversation length for the problem context."""
    if not conversation_history:
        return 0
    student_msgs = [m for m in conversation_history if m.get("role") == "student"]
    return len(student_msgs)


class AnalyzeTeachingRequest(BaseModel):
    student_input: str = ""


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
    teaching_event["quality_score"] = quality

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

    # Evaluate bug if problem context provided
    code_modification = None
    if body.problem_id:
        problems = adapter.load_problems()
        current_problem = next((p for p in problems if p.get("problem_id") == body.problem_id), None)
        if current_problem and current_problem.get("problem_type") == "buggy-code":
            try:
                bug_eval = evaluate_bug_identification(
                    body.student_input, current_problem, conversation_history,
                )
                code_modification = bug_eval.get("code_modification")
            except Exception:
                pass

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
        state_update={"learned": sorted(learned), "code_modification": code_modification},
        ta_response=ta_response,
    )


@router.post("/api/ta/{ta_id}/teach/stream")
def teach_stream(
    ta_id: int,
    body: TeachRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    """Stream TA response via Server-Sent Events. Same as teach but response is streamed chunk-by-chunk."""
    ta = _get_ta(ta_id, current_user.id, db)
    session = get_or_create_teaching_session(db, ta.id)
    set_trace_db_session(db, session.id)
    tracker = get_tracker_for_ta(ta)
    adapter = get_domain_adapter(ta.domain_id)
    unit_ids = [u["id"] for u in adapter.load_knowledge_units()]
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
    teaching_event["quality_score"] = quality
    apply_teaching_event(tracker, teaching_event, new_status="learned")
    conversation_history = []
    for te in db.query(TeachingEvent).filter(TeachingEvent.session_id == session.id).order_by(TeachingEvent.created_at.asc()).all():
        if te.student_input:
            conversation_history.append({"role": "student", "content": te.student_input})
        if te.ta_response:
            conversation_history.append({"role": "ta", "content": te.ta_response})
    learned = list(tracker.get_learned_units())
    active_mis_ids = list(tracker.get_active_misconception_ids(tracker.get_learned_units()))

    # Chat behavior analysis: detect AI-generated paste patterns
    try:
        cheat_analysis = analyze_message_for_cheating(body.student_input)
        if cheat_analysis.get("suspicious"):
            from src.db.models import StudentFlag
            db.add(StudentFlag(
                user_id=current_user.id,
                flag_type="ai_paste_detected",
                severity="warning",
                detail={
                    "gpt_score": cheat_analysis.get("gpt_pattern_score"),
                    "reasons": cheat_analysis.get("reasons"),
                    "input_preview": body.student_input[:200],
                },
                session_id=str(session.id),
            ))
            db.commit()
    except Exception:
        pass

    return StreamingResponse(
        _teach_stream_generator(
            tracker, ta, session, db, teaching_event, adapter,
            conversation_history, learned, active_mis_ids,
            problem_id=body.problem_id,
        ),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
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


@router.post("/api/ta/{ta_id}/analyze-teaching")
def analyze_teaching_endpoint(
    ta_id: int,
    body: AnalyzeTeachingRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    """Teaching Helper: analyze current teaching input for antipatterns (commanding, spoon_feeding, under_teaching)."""
    ta = _get_ta(ta_id, current_user.id, db)
    session = get_or_create_teaching_session(db, ta.id)
    conversation_history = []
    for te in db.query(TeachingEvent).filter(TeachingEvent.session_id == session.id).order_by(TeachingEvent.created_at.asc()).all():
        if te.student_input:
            conversation_history.append({"role": "student", "content": te.student_input})
        if te.ta_response:
            conversation_history.append({"role": "ta", "content": te.ta_response})
    result = analyze_teaching(
        conversation_history,
        body.student_input or "",
        domain=ta.domain_id or "python",
    )
    return result


@router.get("/api/ta/{ta_id}/proactive-checkin")
def proactive_checkin(
    ta_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """
    Generate a lightweight proactive TA check-in message when the conversation is idle.
    This enables TA to ask for clarification/examples without waiting for a new student message.
    """
    ta = _get_ta(ta_id, current_user.id, db)
    session = get_or_create_teaching_session(db, ta.id)
    tracker = get_tracker_for_ta(ta)

    latest_event = (
        db.query(TeachingEvent)
        .filter(TeachingEvent.session_id == session.id)
        .order_by(TeachingEvent.created_at.desc())
        .first()
    )
    if latest_event and latest_event.created_at:
        created_at = latest_event.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        idle_seconds = (datetime.now(timezone.utc) - created_at).total_seconds()
        if idle_seconds < 45:
            return {"message": None, "reason": "not_idle_enough"}

    learned = sorted(tracker.get_learned_units())
    active_mis_ids = list(tracker.get_active_misconception_ids(learned))

    if active_mis_ids:
        message = f"I'm still confused about {active_mis_ids[0]}. Could you explain it with one concrete example?"
        return {"message": message, "reason": "active_misconception"}

    if learned:
        latest_unit = learned[-1]
        message = f"Can we do one more quick example for {latest_unit} so I can check if I really understand it?"
        return {"message": message, "reason": "reinforce_latest_learning"}

    return {
        "message": "Could you teach me one small foundational concept first, then test me with a tiny exercise?",
        "reason": "bootstrap_learning",
    }
