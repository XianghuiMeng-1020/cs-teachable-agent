"""
Stage One: Structured teaching event format.
Makes the teaching step explicit and inspectable (no natural language understanding).
"""

import uuid


def make_teaching_event(
    topic_taught: str,
    knowledge_units_taught: list[str],
    note: str = "",
    teaching_event_id: str | None = None,
) -> dict:
    """
    Create a structured teaching event.
    - topic_taught: short label (e.g. "Variables and print")
    - knowledge_units_taught: list of KU ids from seed
    - note: optional short teaching note for inspection
    - teaching_event_id: optional id for trace; generated if not provided
    """
    event = {
        "topic_taught": topic_taught,
        "knowledge_units_taught": knowledge_units_taught,
        "note": note,
    }
    event["teaching_event_id"] = teaching_event_id or str(uuid.uuid4())
    return event


def apply_teaching_event(tracker, event: dict, new_status: str = "learned") -> None:
    """
    Apply a teaching event to the state tracker.
    Only updates units that exist in the tracker; ignores unknown unit ids.
    When tracker supports it, appends teaching_evidence per unit (state_before -> state_after).
    """
    unit_ids = event.get("knowledge_units_taught", [])
    teaching_event_id = event.get("teaching_event_id")
    tracker.update_after_teaching(
        unit_ids,
        new_status=new_status,
        teaching_event=event,
        teaching_event_id=teaching_event_id,
    )
