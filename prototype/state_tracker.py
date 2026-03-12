"""
Stage One: TA knowledge state tracker.
Source of truth: seed/knowledge-units-stage1.json.
All units start unknown; updates come only from teaching events.
"""

import json
from pathlib import Path


def load_knowledge_units(path: Path) -> list[dict]:
    """Load knowledge unit definitions from JSON."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("knowledge_units", [])


class StateTracker:
    """Tracks per-KU status. Knowledge state is the only source of truth for what the TA 'knows'."""

    STATUS_UNKNOWN = "unknown"
    STATUS_PARTIALLY_LEARNED = "partially_learned"
    STATUS_LEARNED = "learned"

    def __init__(self, knowledge_units_path: Path):
        self._units = {u["id"]: u for u in load_knowledge_units(knowledge_units_path)}
        self._state: dict[str, str] = {uid: self.STATUS_UNKNOWN for uid in self._units}

    def get_state(self) -> dict[str, str]:
        """Return full state: unit_id -> status."""
        return dict(self._state)

    def get_learned_units(self) -> set[str]:
        """Return set of unit IDs that are partially_learned or learned (TA can use these)."""
        return {
            uid for uid, status in self._state.items()
            if status in (self.STATUS_PARTIALLY_LEARNED, self.STATUS_LEARNED)
        }

    def update_after_teaching(self, unit_ids: list[str], new_status: str = STATUS_LEARNED) -> None:
        """Update state after one teaching event. Only listed units are updated."""
        for uid in unit_ids:
            if uid in self._state:
                self._state[uid] = new_status

    def get_unit_ids(self) -> set[str]:
        """All known unit IDs (from seed file)."""
        return set(self._units.keys())
