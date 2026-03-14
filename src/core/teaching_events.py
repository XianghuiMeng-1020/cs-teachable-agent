"""Structured teaching event format. Makes the teaching step explicit and inspectable."""

import uuid


def make_teaching_event(
    topic_taught: str,
    knowledge_units_taught: list[str],
    note: str = "",
    teaching_event_id: str | None = None,
) -> dict:
    """Create a structured teaching event."""
    event = {
        "topic_taught": topic_taught,
        "knowledge_units_taught": knowledge_units_taught,
        "note": note,
    }
    event["teaching_event_id"] = teaching_event_id or str(uuid.uuid4())
    return event


def apply_teaching_event(tracker, event: dict, new_status: str = "learned") -> None:
    """Apply a teaching event to the state tracker."""
    unit_ids = event.get("knowledge_units_taught", [])
    teaching_event_id = event.get("teaching_event_id")
    tracker.update_after_teaching(
        unit_ids,
        new_status=new_status,
        teaching_event=event,
        teaching_event_id=teaching_event_id,
    )
