"""
Stage One: Structured teaching event format.
Makes the teaching step explicit and inspectable (no natural language understanding).
"""


def make_teaching_event(
    topic_taught: str,
    knowledge_units_taught: list[str],
    note: str = "",
) -> dict:
    """
    Create a structured teaching event.
    - topic_taught: short label (e.g. "Variables and print")
    - knowledge_units_taught: list of KU ids from seed
    - note: optional short teaching note for inspection
    """
    return {
        "topic_taught": topic_taught,
        "knowledge_units_taught": knowledge_units_taught,
        "note": note,
    }


def apply_teaching_event(tracker, event: dict, new_status: str = "learned") -> None:
    """
    Apply a teaching event to the state tracker.
    Only updates units that exist in the tracker; ignores unknown unit ids.
    """
    unit_ids = event.get("knowledge_units_taught", [])
    tracker.update_after_teaching(unit_ids, new_status=new_status)
