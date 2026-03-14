"""
Misconception engine: activate, correct (unlearn), and relearn.
Uses trace layer for recording events.
"""

import uuid

from src.core.trace import (
    record_misconception_activation,
    record_correction_event,
    record_relearning_event,
)


def activate_misconception_for_unit(
    tracker,
    unit_id: str,
    misconception_id: str,
    trigger: str = "pre_seeded",
    trigger_reference: str | None = None,
) -> bool:
    """Activate a misconception for the given unit. Records trace event."""
    if unit_id not in tracker.get_unit_ids():
        return False
    state_before = tracker.get_state().get(unit_id, "unknown")
    added = tracker.activate_misconception(
        unit_id,
        misconception_id,
        trigger=trigger,
        trigger_reference=trigger_reference,
        set_status_to_misconception=False,
    )
    if not added:
        return False
    state_after = tracker.get_state().get(unit_id, "unknown")
    record_misconception_activation(
        domain=tracker.get_domain(),
        unit_id=unit_id,
        misconception_id=misconception_id,
        trigger=trigger,
        trigger_reference=trigger_reference,
        state_before=state_before,
        state_after=state_after,
    )
    return True


def apply_correction(
    tracker,
    unit_id: str,
    misconception_id: str,
    trigger: str = "explicit_correction_event",
    teaching_event_id: str | None = None,
    correction_event_id: str | None = None,
) -> bool:
    """Apply unlearning: remove misconception, set status to corrected, record trace."""
    state_before = tracker.get_state().get(unit_id, "unknown")
    ok = tracker.apply_unlearning(
        unit_id,
        misconception_id,
        trigger=trigger,
        teaching_event_id=teaching_event_id,
        correction_event_id=correction_event_id,
    )
    if not ok:
        return False
    record_correction_event(
        domain=tracker.get_domain(),
        unit_id=unit_id,
        misconception_id=misconception_id,
        trigger=trigger,
        state_before=state_before,
        state_after=tracker.STATUS_CORRECTED,
        teaching_event_id=teaching_event_id,
        correction_event_id=correction_event_id,
    )
    return True


RELEARNING_MIN_EVENTS = 1


def add_relearning_evidence_from_teaching(
    tracker,
    unit_id: str,
    teaching_event_id: str,
    *,
    min_relearning_events: int = RELEARNING_MIN_EVENTS,
) -> bool:
    """Append relearning_evidence (type=teaching), then try transition to learned."""
    if unit_id not in tracker.get_unit_ids():
        return False
    rec = tracker.get_unit_record(unit_id)
    if rec and rec.get("status") != tracker.STATUS_CORRECTED:
        return False
    relearning_event_id = str(uuid.uuid4())
    tracker.append_relearning_evidence(
        unit_id,
        relearning_event_id=relearning_event_id,
        event_type="teaching",
        reference_id=teaching_event_id,
    )
    tracker.try_relearning_transition(
        unit_id,
        require_correction=True,
        min_relearning_events=min_relearning_events,
    )
    record_relearning_event(
        domain=tracker.get_domain(),
        unit_id=unit_id,
        relearning_event_id=relearning_event_id,
        event_type="teaching",
        state_after=tracker.get_state().get(unit_id, ""),
        reference_id=teaching_event_id,
    )
    return True


def add_relearning_evidence_from_successful_task(
    tracker,
    unit_id: str,
    attempt_id: str,
    *,
    min_relearning_events: int = RELEARNING_MIN_EVENTS,
) -> bool:
    """Append relearning_evidence (type=successful_task), then try transition to learned."""
    if unit_id not in tracker.get_unit_ids():
        return False
    rec = tracker.get_unit_record(unit_id)
    if rec and rec.get("status") != tracker.STATUS_CORRECTED:
        return False
    relearning_event_id = str(uuid.uuid4())
    tracker.append_relearning_evidence(
        unit_id,
        relearning_event_id=relearning_event_id,
        event_type="successful_task",
        reference_id=attempt_id,
    )
    tracker.try_relearning_transition(
        unit_id,
        require_correction=True,
        min_relearning_events=min_relearning_events,
    )
    record_relearning_event(
        domain=tracker.get_domain(),
        unit_id=unit_id,
        relearning_event_id=relearning_event_id,
        event_type="successful_task",
        state_after=tracker.get_state().get(unit_id, ""),
        reference_id=attempt_id,
    )
    return True
