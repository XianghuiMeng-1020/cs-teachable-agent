"""
Stage D: Structured correction event for explicit misconception correction.
Supports: unit_id, misconception_id, trigger, optional teaching_event_id.
Correction is driven by a structured event (no natural-language parsing yet).
"""

import uuid


def make_correction_event(
    unit_id: str,
    misconception_id: str,
    trigger: str = "explicit_correction_event",
    teaching_event_id: str | None = None,
    correction_event_id: str | None = None,
) -> dict:
    """
    Create a structured correction event for an active misconception.
    - unit_id: knowledge unit being corrected
    - misconception_id: which misconception is being corrected
    - trigger: e.g. "explicit_correction_event", "student_reteaching"
    - teaching_event_id: optional link to the teaching event that delivered the correction
    - correction_event_id: optional id for trace; generated if not provided
    """
    return {
        "unit_id": unit_id,
        "misconception_id": misconception_id,
        "trigger": trigger,
        "teaching_event_id": teaching_event_id,
        "correction_event_id": correction_event_id or str(uuid.uuid4()),
    }
