"""Adaptive learning: recommend next KUs from prerequisites and current state."""

from __future__ import annotations

def recommend_next_kus(
    knowledge_unit_definitions: list[dict],
    learned_ids: set[str],
) -> list[dict]:
    """Return KUs that are unlocked (all prerequisites learned) but not yet learned, in order."""
    by_id = {u["id"]: u for u in knowledge_unit_definitions}
    result = []
    for u in knowledge_unit_definitions:
        ku_id = u.get("id")
        if not ku_id or ku_id in learned_ids:
            continue
        prereqs = set(u.get("prerequisites") or [])
        if prereqs and not prereqs.issubset(learned_ids):
            continue
        result.append({
            "id": ku_id,
            "name": u.get("name", ku_id),
            "topic_group": u.get("topic_group"),
            "prerequisites": list(prereqs),
        })
    return result


def estimate_minutes_per_ku() -> int:
    """Rough estimate: minutes to learn one KU (for completion time)."""
    return 5
