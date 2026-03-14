"""
Trace and History Layer. Records the evidence chain so one complete
teaching–testing cycle can be reconstructed.
Event types: teaching_event, knowledge_state_update, learner_dialogue,
task_selection, ta_attempt, evaluation_result, mastery_update,
misconception_activation, correction_event, relearning_event.
"""

import time
import uuid
from typing import Any

_trace_events: list[dict] = []
_sequence_counter: int = 0
_db_session = None
_teaching_session_id = None


def set_trace_db_session(db, teaching_session_id: int | None):
    """Inject DB session and teaching session id so record_* can persist to TraceEvent table."""
    global _db_session, _teaching_session_id
    _db_session = db
    _teaching_session_id = teaching_session_id


def _write_trace_to_db(event_type: str, payload: dict) -> None:
    """If DB session is set, insert one TraceEvent row."""
    if _db_session is None or _teaching_session_id is None:
        return
    try:
        from src.db.models import TraceEvent
        row = TraceEvent(
            session_id=_teaching_session_id,
            event_type=event_type,
            payload=payload,
        )
        _db_session.add(row)
        _db_session.commit()
    except Exception:
        pass


def _next_id() -> str:
    return str(uuid.uuid4())


def _sequence_and_ts() -> tuple[int, str]:
    t = time.time()
    return (int(t * 1_000_000), f"{t:.6f}")


def _next_sequence() -> int:
    global _sequence_counter
    _sequence_counter += 1
    return _sequence_counter


def get_trace_events() -> list[dict]:
    """Return all recorded events (copy)."""
    return list(_trace_events)


def clear_trace() -> None:
    """Clear the in-memory trace."""
    global _trace_events, _sequence_counter
    _trace_events = []
    _sequence_counter = 0


def record_teaching_event(
    domain: str,
    topic_taught: str = "",
    knowledge_units_taught: list[str] | None = None,
    note: str = "",
    teaching_event_id: str | None = None,
    session_id: str | None = None,
) -> str:
    event_id = teaching_event_id or _next_id()
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "teaching_event",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "topic_taught": topic_taught,
        "knowledge_units_taught": knowledge_units_taught or [],
        "note": note,
        "session_id": session_id,
    }
    _trace_events.append(payload)
    _write_trace_to_db("teaching_event", payload)
    return event_id


def record_knowledge_state_update(
    domain: str,
    trigger: str,
    unit_ids: list[str],
    state_before: Any,
    state_after: Any,
    evidence_source: str | None = None,
) -> str:
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "knowledge_state_update",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "trigger": trigger,
        "unit_ids": unit_ids,
        "state_before": state_before,
        "state_after": state_after,
        "evidence_source": evidence_source,
    }
    _trace_events.append(payload)
    _write_trace_to_db("knowledge_state_update", payload)
    return event_id


def record_learner_dialogue(
    domain: str,
    teaching_event_id: str,
    learned_unit_ids: list[str],
    response_text: str,
    active_misconception_ids: list[str] | None = None,
) -> str:
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "learner_dialogue",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "teaching_event_id": teaching_event_id,
        "learned_unit_ids": learned_unit_ids,
        "active_misconception_ids": active_misconception_ids or [],
        "response_text": response_text,
    }
    _trace_events.append(payload)
    _write_trace_to_db("learner_dialogue", payload)
    return event_id


def record_task_selection(
    domain: str,
    eligible_unit_ids: list[str],
    selected_task_id: str | None,
    eligible_task_ids: list[str] | None = None,
    ineligible_reasons: list[dict] | None = None,
) -> str:
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "task_selection",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "eligible_unit_ids": eligible_unit_ids,
        "selected_task_id": selected_task_id,
        "eligible_task_ids": eligible_task_ids or [],
        "ineligible_reasons": ineligible_reasons or [],
    }
    _trace_events.append(payload)
    _write_trace_to_db("task_selection", payload)
    return event_id


def record_ta_attempt(
    domain: str,
    task_id: str,
    attempt_id: str,
    learned_unit_ids: list[str],
    output_summary: str,
    guard_passed: bool = True,
    fallback_used: bool = False,
    active_misconception_ids: list[str] | None = None,
) -> str:
    event_id = attempt_id
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "ta_attempt",
        "event_id": event_id,
        "attempt_id": attempt_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "task_id": task_id,
        "learned_unit_ids": learned_unit_ids,
        "active_misconception_ids": active_misconception_ids or [],
        "output_summary": output_summary,
        "guard_passed": guard_passed,
        "fallback_used": fallback_used,
    }
    _trace_events.append(payload)
    _write_trace_to_db("ta_attempt", payload)
    return event_id


def record_evaluation_result(
    domain: str,
    task_id: str,
    attempt_id: str,
    pass_fail: bool,
    unit_ids_tested: list[str],
    mastery_level_before: Any = None,
    mastery_level_after: Any = None,
    misconception_active_during_attempt: str | None = None,
) -> str:
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "evaluation_result",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "task_id": task_id,
        "attempt_id": attempt_id,
        "pass_fail": pass_fail,
        "unit_ids_tested": unit_ids_tested,
        "mastery_level_before": mastery_level_before,
        "mastery_level_after": mastery_level_after,
        "misconception_active_during_attempt": misconception_active_during_attempt,
    }
    _trace_events.append(payload)
    _write_trace_to_db("evaluation_result", payload)
    return event_id


def record_mastery_update(
    domain: str,
    unit_id: str | None,
    mastery_level: str,
    pass_rate: float | None = None,
    attempt_count: int | None = None,
    trigger: str | None = None,
) -> str:
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "mastery_update",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "unit_id": unit_id,
        "mastery_level": mastery_level,
        "pass_rate": pass_rate,
        "attempt_count": attempt_count,
        "trigger": trigger,
    }
    _trace_events.append(payload)
    _write_trace_to_db("mastery_update", payload)
    return event_id


def record_misconception_activation(
    domain: str,
    unit_id: str,
    misconception_id: str,
    trigger: str,
    trigger_reference: str | None = None,
    state_before: Any = None,
    state_after: Any = None,
) -> str:
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "misconception_activation",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "unit_id": unit_id,
        "misconception_id": misconception_id,
        "trigger": trigger,
        "trigger_reference": trigger_reference,
        "state_before": state_before,
        "state_after": state_after,
    }
    _trace_events.append(payload)
    _write_trace_to_db("misconception_activation", payload)
    return event_id


def record_correction_event(
    domain: str,
    unit_id: str,
    misconception_id: str,
    trigger: str,
    state_before: Any,
    state_after: Any,
    teaching_event_id: str | None = None,
    correction_event_id: str | None = None,
) -> str:
    event_id = correction_event_id or _next_id()
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "correction_event",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "unit_id": unit_id,
        "misconception_id": misconception_id,
        "trigger": trigger,
        "teaching_event_id": teaching_event_id,
        "state_before": state_before,
        "state_after": state_after,
    }
    _trace_events.append(payload)
    _write_trace_to_db("correction_event", payload)
    return event_id


def record_relearning_event(
    domain: str,
    unit_id: str,
    relearning_event_id: str,
    event_type: str,
    state_after: Any,
    reference_id: str | None = None,
) -> str:
    _, ts = _sequence_and_ts()
    payload = {
        "event_type": "relearning_event",
        "event_id": relearning_event_id,
        "relearning_event_id": relearning_event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "unit_id": unit_id,
        "type": event_type,
        "state_after": state_after,
        "reference_id": reference_id,
    }
    _trace_events.append(payload)
    _write_trace_to_db("relearning_event", payload)
    return relearning_event_id
