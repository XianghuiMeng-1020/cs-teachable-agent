"""
TA knowledge state tracker.
Source of truth: knowledge units from domain seed.
All units start unknown; updates come only from teaching events.
Per-unit: status, confidence, active_misconceptions, evidence, mastery_history.
"""

import json
import time
import uuid
from pathlib import Path


def load_knowledge_units_from_path(path: Path) -> list[dict]:
    """Load knowledge unit definitions from JSON file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("knowledge_units", [])


def _make_unit_record(unit_def: dict, domain: str, status: str) -> dict:
    """Build one per-unit state record per schema."""
    uid = unit_def.get("id", "")
    return {
        "knowledge_unit_id": uid,
        "knowledge_unit_name": unit_def.get("name", uid),
        "domain": domain,
        "status": status,
        "confidence": 0.0,
        "active_misconceptions": [],
        "teaching_evidence": [],
        "testing_evidence": [],
        "correction_evidence": [],
        "relearning_evidence": [],
        "mastery_history": [],
        "last_updated": _timestamp(),
    }


def _timestamp() -> str:
    return f"{time.time():.6f}"


class StateTracker:
    """
    Tracks per-KU state. Knowledge state is the only source of truth for what the TA 'knows'.
    Can be initialized from a path (legacy) or from a list of unit definitions (domain adapter).
    """

    STATUS_UNKNOWN = "unknown"
    STATUS_PARTIALLY_LEARNED = "partially_learned"
    STATUS_LEARNED = "learned"
    STATUS_MISCONCEPTION = "misconception"
    STATUS_CORRECTED = "corrected"

    DEFAULT_DOMAIN = "python"
    SCHEMA_VERSION = "1.0"

    def __init__(
        self,
        knowledge_units_path: Path | None = None,
        unit_definitions: list[dict] | None = None,
        domain: str | None = None,
    ):
        self._domain = domain or self.DEFAULT_DOMAIN
        self._schema_version = self.SCHEMA_VERSION
        self._last_updated = _timestamp()
        if unit_definitions is not None:
            units_list = unit_definitions
        elif knowledge_units_path is not None:
            units_list = load_knowledge_units_from_path(knowledge_units_path)
        else:
            units_list = []
        self._units = {u["id"]: u for u in units_list}
        self._state: dict[str, dict] = {}
        for uid, u in self._units.items():
            self._state[uid] = _make_unit_record(u, self._domain, self.STATUS_UNKNOWN)

    def get_domain(self) -> str:
        return self._domain

    def get_schema_version(self) -> str:
        return self._schema_version

    def get_state(self) -> dict[str, str]:
        """Legacy view: unit_id -> status."""
        return {uid: rec["status"] for uid, rec in self._state.items()}

    def get_full_state(self) -> dict:
        self._last_updated = _timestamp()
        return {
            "domain": self._domain,
            "schema_version": self._schema_version,
            "last_updated": self._last_updated,
            "units": dict(self._state),
        }

    def get_learned_units(self) -> set[str]:
        return {
            uid
            for uid, rec in self._state.items()
            if rec["status"] in (self.STATUS_PARTIALLY_LEARNED, self.STATUS_LEARNED)
        }

    def is_unit_corrected(self, unit_id: str) -> bool:
        rec = self._state.get(unit_id, {})
        return rec.get("status") == self.STATUS_CORRECTED

    def get_eligible_units(self) -> set[str]:
        return self.get_learned_units()

    def get_active_misconceptions(self, unit_id: str | None = None) -> list[dict]:
        if unit_id:
            rec = self._state.get(unit_id, {})
            return list(rec.get("active_misconceptions", []))
        out: list[dict] = []
        for rec in self._state.values():
            out.extend(rec.get("active_misconceptions", []))
        return out

    def get_active_misconception_ids(self, unit_ids: set[str] | None = None) -> list[str]:
        if unit_ids is None:
            unit_ids = set(self._state.keys())
        seen: set[str] = set()
        out: list[str] = []
        for uid in unit_ids:
            for rec in self._state.get(uid, {}).get("active_misconceptions", []):
                mid = rec.get("misconception_id", "")
                if mid and mid not in seen:
                    seen.add(mid)
                    out.append(mid)
        return out

    def activate_misconception(
        self,
        unit_id: str,
        misconception_id: str,
        trigger: str = "pre_seeded",
        trigger_reference: str | None = None,
        *,
        set_status_to_misconception: bool = False,
    ) -> bool:
        if unit_id not in self._state:
            return False
        rec = self._state[unit_id]
        for m in rec.get("active_misconceptions", []):
            if m.get("misconception_id") == misconception_id:
                return False
        now = _timestamp()
        rec["active_misconceptions"].append({
            "misconception_id": misconception_id,
            "activated_at": now,
            "trigger": trigger,
            "trigger_reference": trigger_reference,
            "flagged_for_correction": False,
        })
        rec["last_updated"] = now
        self._last_updated = now
        if set_status_to_misconception:
            rec["status"] = self.STATUS_MISCONCEPTION
        return True

    def update_after_teaching(
        self,
        unit_ids: list[str],
        new_status: str = STATUS_LEARNED,
        *,
        teaching_event: dict | None = None,
        teaching_event_id: str | None = None,
    ) -> None:
        event_id = teaching_event_id or (str(uuid.uuid4()) if teaching_event else None)
        topic = teaching_event.get("topic_taught", "") if teaching_event else ""
        note = teaching_event.get("note", "") if teaching_event else ""
        units_taught = (
            teaching_event.get("knowledge_units_taught", unit_ids) if teaching_event else unit_ids
        )
        now = _timestamp()
        self._last_updated = now
        for uid in unit_ids:
            if uid not in self._state:
                continue
            rec = self._state[uid]
            state_before = rec["status"]
            rec["status"] = new_status
            rec["last_updated"] = now
            if new_status == self.STATUS_LEARNED and rec["confidence"] < 0.8:
                rec["confidence"] = 0.8
            if event_id is not None:
                rec["teaching_evidence"].append({
                    "teaching_event_id": event_id,
                    "timestamp": now,
                    "topic_taught": topic,
                    "knowledge_units_taught": list(units_taught),
                    "state_before": state_before,
                    "state_after": new_status,
                    "misconception_activated": None,
                    "note": note,
                })

    def mark_taught(self, unit_ids: list[str], new_status: str = STATUS_LEARNED) -> None:
        for uid in unit_ids:
            if uid in self._state:
                self._state[uid]["status"] = new_status
                self._state[uid]["last_updated"] = _timestamp()
        self._last_updated = _timestamp()

    def append_teaching_evidence(
        self,
        unit_id: str,
        teaching_event_id: str,
        state_before: str,
        state_after: str,
        topic_taught: str = "",
        knowledge_units_taught: list[str] | None = None,
        note: str = "",
    ) -> None:
        if unit_id not in self._state:
            return
        rec = self._state[unit_id]
        rec["teaching_evidence"].append({
            "teaching_event_id": teaching_event_id,
            "timestamp": _timestamp(),
            "topic_taught": topic_taught,
            "knowledge_units_taught": knowledge_units_taught or [unit_id],
            "state_before": state_before,
            "state_after": state_after,
            "misconception_activated": None,
            "note": note,
        })
        rec["last_updated"] = _timestamp()
        self._last_updated = rec["last_updated"]

    def apply_unlearning(
        self,
        unit_id: str,
        misconception_id: str,
        trigger: str = "explicit_correction_event",
        teaching_event_id: str | None = None,
        correction_event_id: str | None = None,
    ) -> bool:
        if unit_id not in self._state:
            return False
        rec = self._state[unit_id]
        active = rec.get("active_misconceptions", [])
        state_before = rec["status"]
        new_active = [m for m in active if m.get("misconception_id") != misconception_id]
        if len(new_active) == len(active):
            return False
        rec["active_misconceptions"] = new_active
        rec["status"] = self.STATUS_CORRECTED
        now = _timestamp()
        rec["last_updated"] = now
        self._last_updated = now
        rec["correction_evidence"].append({
            "misconception_id": misconception_id,
            "corrected_at": now,
            "trigger": trigger,
            "teaching_event_id": teaching_event_id,
            "correction_event_id": correction_event_id,
            "state_before": state_before,
            "state_after": self.STATUS_CORRECTED,
        })
        return True

    def append_correction_evidence(
        self,
        unit_id: str,
        misconception_id: str,
        corrected_at: str,
        trigger: str,
        state_before: str,
        state_after: str,
        teaching_event_id: str | None = None,
        correction_event_id: str | None = None,
    ) -> None:
        if unit_id not in self._state:
            return
        rec = self._state[unit_id]
        rec["correction_evidence"].append({
            "misconception_id": misconception_id,
            "corrected_at": corrected_at,
            "trigger": trigger,
            "teaching_event_id": teaching_event_id,
            "correction_event_id": correction_event_id,
            "state_before": state_before,
            "state_after": state_after,
        })
        rec["last_updated"] = _timestamp()
        self._last_updated = rec["last_updated"]

    def append_relearning_evidence(
        self,
        unit_id: str,
        relearning_event_id: str,
        event_type: str,
        reference_id: str | None = None,
    ) -> None:
        if unit_id not in self._state:
            return
        rec = self._state[unit_id]
        now = _timestamp()
        rec["relearning_evidence"].append({
            "relearning_event_id": relearning_event_id,
            "timestamp": now,
            "type": event_type,
            "state_after": rec["status"],
            "reference_id": reference_id,
        })
        rec["last_updated"] = now
        self._last_updated = now

    def try_relearning_transition(
        self,
        unit_id: str,
        *,
        require_correction: bool = True,
        min_relearning_events: int = 1,
    ) -> bool:
        if unit_id not in self._state:
            return False
        rec = self._state[unit_id]
        if rec["status"] != self.STATUS_CORRECTED:
            return False
        if require_correction and not rec.get("correction_evidence"):
            return False
        relearning = rec.get("relearning_evidence", [])
        if len(relearning) < min_relearning_events:
            return False
        rec["status"] = self.STATUS_LEARNED
        rec["last_updated"] = _timestamp()
        self._last_updated = rec["last_updated"]
        if rec["confidence"] < 0.8:
            rec["confidence"] = 0.8
        return True

    def append_testing_evidence(
        self,
        unit_id: str,
        task_id: str,
        attempt_id: str,
        pass_fail: bool,
        timestamp: str | None = None,
        mastery_level_at_attempt: str | None = None,
        misconception_active_during_attempt: str | None = None,
    ) -> None:
        if unit_id not in self._state:
            return
        rec = self._state[unit_id]
        rec["testing_evidence"].append({
            "task_id": task_id,
            "attempt_id": attempt_id,
            "timestamp": timestamp or _timestamp(),
            "pass_fail": pass_fail,
            "mastery_level_at_attempt": mastery_level_at_attempt,
            "misconception_active_during_attempt": misconception_active_during_attempt,
        })
        rec["last_updated"] = _timestamp()
        self._last_updated = rec["last_updated"]

    def append_mastery_history(
        self,
        unit_id: str,
        mastery_level: str,
        pass_rate: float | None = None,
        attempt_count: int | None = None,
        trigger: str | None = None,
    ) -> None:
        if unit_id not in self._state:
            return
        rec = self._state[unit_id]
        rec["mastery_history"].append({
            "timestamp": _timestamp(),
            "mastery_level": mastery_level,
            "pass_rate": pass_rate,
            "attempt_count": attempt_count,
            "trigger": trigger,
        })
        rec["last_updated"] = _timestamp()
        self._last_updated = rec["last_updated"]

    PERIOD_BEFORE_MISCONCEPTION = "before_misconception"
    PERIOD_DURING_MISCONCEPTION = "during_misconception"
    PERIOD_AFTER_CORRECTION = "after_correction"

    def append_mastery_history_entry(
        self,
        unit_id: str,
        attempt_id: str,
        problem_id: str,
        pass_fail: bool,
        mastery_level: str,
        *,
        misconception_active_during_attempt: str | None = None,
        period: str | None = None,
        note: str | None = None,
    ) -> None:
        if unit_id not in self._state:
            return
        rec = self._state[unit_id]
        now = _timestamp()
        rec["mastery_history"].append({
            "timestamp": now,
            "attempt_id": attempt_id,
            "problem_id": problem_id,
            "pass_fail": pass_fail,
            "mastery_level": mastery_level,
            "misconception_active_during_attempt": misconception_active_during_attempt,
            "period": period,
            "note": note,
        })
        rec["last_updated"] = now
        self._last_updated = now

    def get_mastery_history(self, unit_id: str) -> list[dict]:
        if unit_id not in self._state:
            return []
        return list(self._state[unit_id].get("mastery_history", []))

    def get_unit_ids(self) -> set[str]:
        return set(self._units.keys())

    def get_unit_record(self, unit_id: str) -> dict | None:
        return dict(self._state[unit_id]) if unit_id in self._state else None
