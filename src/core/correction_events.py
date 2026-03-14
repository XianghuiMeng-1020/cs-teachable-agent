"""Structured correction event for explicit misconception correction."""

import uuid


def make_correction_event(
    unit_id: str,
    misconception_id: str,
    trigger: str = "explicit_correction_event",
    teaching_event_id: str | None = None,
    correction_event_id: str | None = None,
) -> dict:
    """Create a structured correction event for an active misconception."""
    return {
        "unit_id": unit_id,
        "misconception_id": misconception_id,
        "trigger": trigger,
        "teaching_event_id": teaching_event_id,
        "correction_event_id": correction_event_id or str(uuid.uuid4()),
    }
