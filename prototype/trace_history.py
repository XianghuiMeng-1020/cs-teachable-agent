"""
Trace and History Layer (Stage B).
Records the evidence chain per TRACE_AND_HISTORY_LAYER.md so one complete
teaching–testing cycle can be reconstructed: teaching → state update → dialogue
→ task selection → TA attempt → evaluation → mastery update.
Event types: teaching_event, knowledge_state_update, learner_dialogue,
task_selection, ta_attempt, evaluation_result, mastery_update.
Stage C: misconception_activation is recorded when a misconception is activated for a unit.
"""

import time
import uuid
from typing import Any


def _next_id() -> str:
    return str(uuid.uuid4())


def _sequence_and_ts() -> tuple[int, str]:
    """Return (sequence_id, timestamp) for ordering."""
    t = time.time()
    return (int(t * 1_000_000), f"{t:.6f}")


# In-memory trace store for the prototype. One list per run; cleared when a new TraceRecorder is used.
_trace_events: list[dict] = []
_sequence_counter: int = 0


def _next_sequence() -> int:
    global _sequence_counter
    _sequence_counter += 1
    return _sequence_counter


def get_trace_events() -> list[dict]:
    """Return all recorded events (copy). Used for inspection and evaluation."""
    return list(_trace_events)


def clear_trace() -> None:
    """Clear the in-memory trace (e.g. at start of a new scenario or run)."""
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
    """Record a teaching_event. Returns event_id for linking."""
    event_id = teaching_event_id or _next_id()
    seq, ts = _sequence_and_ts()
    _trace_events.append({
        "event_type": "teaching_event",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "topic_taught": topic_taught,
        "knowledge_units_taught": knowledge_units_taught or [],
        "note": note,
        "session_id": session_id,
    })
    return event_id


def record_knowledge_state_update(
    domain: str,
    trigger: str,
    unit_ids: list[str],
    state_before: Any,
    state_after: Any,
    evidence_source: str | None = None,
) -> str:
    """Record a knowledge_state_update (after teaching, correction, etc.)."""
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    _trace_events.append({
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
    })
    return event_id


def record_learner_dialogue(
    domain: str,
    teaching_event_id: str,
    learned_unit_ids: list[str],
    response_text: str,
    active_misconception_ids: list[str] | None = None,
) -> str:
    """Record learner_dialogue (TA response after teaching)."""
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    _trace_events.append({
        "event_type": "learner_dialogue",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "teaching_event_id": teaching_event_id,
        "learned_unit_ids": learned_unit_ids,
        "active_misconception_ids": active_misconception_ids or [],
        "response_text": response_text,
    })
    return event_id


def record_task_selection(
    domain: str,
    eligible_unit_ids: list[str],
    selected_task_id: str | None,
    eligible_task_ids: list[str] | None = None,
    ineligible_reasons: list[dict] | None = None,
) -> str:
    """Record task_selection (which task was chosen or that none was eligible)."""
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    _trace_events.append({
        "event_type": "task_selection",
        "event_id": event_id,
        "sequence_id": _next_sequence(),
        "timestamp": ts,
        "domain": domain,
        "eligible_unit_ids": eligible_unit_ids,
        "selected_task_id": selected_task_id,
        "eligible_task_ids": eligible_task_ids or [],
        "ineligible_reasons": ineligible_reasons or [],
    })
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
    """Record ta_attempt (TA code/attempt for a task)."""
    event_id = attempt_id
    _, ts = _sequence_and_ts()
    _trace_events.append({
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
    })
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
    """Record evaluation_result (pass/fail and optional mastery delta)."""
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    _trace_events.append({
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
    })
    return event_id


def record_mastery_update(
    domain: str,
    unit_id: str | None,
    mastery_level: str,
    pass_rate: float | None = None,
    attempt_count: int | None = None,
    trigger: str | None = None,
) -> str:
    """Record mastery_update (per-unit or overall mastery level updated)."""
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    _trace_events.append({
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
    })
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
    """
    Record misconception_activation (Stage C).
    When a misconception is activated for a unit: event_id, timestamp/sequence_id,
    domain, unit_id, misconception_id, trigger, trigger_reference, prior state, updated state.
    """
    event_id = _next_id()
    _, ts = _sequence_and_ts()
    _trace_events.append({
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
    })
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
    """
    Record correction_event (unlearning) — Stage D.
    Minimum fields: event_id, timestamp/sequence_id, domain, unit_id, misconception_id,
    trigger, teaching_event_id (optional), state_before, state_after.
    """
    event_id = correction_event_id or _next_id()
    _, ts = _sequence_and_ts()
    _trace_events.append({
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
    })
    return event_id


def record_relearning_event(
    domain: str,
    unit_id: str,
    relearning_event_id: str,
    event_type: str,
    state_after: Any,
    reference_id: str | None = None,
) -> str:
    """
    Record relearning_event — Stage D.
    Minimum fields: event_id/relearning_event_id, timestamp/sequence_id, domain,
    unit_id, type (teaching | successful_task), state_after, reference_id (optional).
    """
    _, ts = _sequence_and_ts()
    _trace_events.append({
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
    })
    return relearning_event_id
