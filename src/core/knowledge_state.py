"""
TA knowledge state tracker.
Source of truth: knowledge units from domain seed.
Per-unit: status, confidence (from BKT), BKT params, active_misconceptions, evidence, mastery_history.
Supports Bayesian Knowledge Tracing (BKT), knowledge decay, and prerequisite-aware updates.
"""

import json
import math
import time
import uuid
from pathlib import Path

# BKT default parameters (research-typical values)
DEFAULT_P_SLIP = 0.1
DEFAULT_P_GUESS = 0.25
DEFAULT_P_TRANSIT = 0.1
DEFAULT_P_KNOW_INIT = 0.01
# Decay: p_know_decayed = p_know * exp(-DECAY_LAMBDA * days_since_practice)
DECAY_LAMBDA = 0.1
# Thresholds for status derivation from p_know
THRESHOLD_LEARNED = 0.85
THRESHOLD_PARTIALLY_LEARNED = 0.5
# Prerequisite: if any prereq has p_know below this, cap p_transit for this unit
PREREQ_MIN_P_KNOW = 0.5

# P-01: Assessment-type specific BKT parameters
ASSESSMENT_TYPE_PARAMS: dict[str, dict[str, float]] = {
    "parsons": {"p_guess": 0.15, "p_slip": 0.08},
    "dropdown": {"p_guess": 0.30, "p_slip": 0.12},
    "execution_trace": {"p_guess": 0.20, "p_slip": 0.10},
    "fill_in_blank": {"p_guess": 0.25, "p_slip": 0.10},
    "open_response": {"p_guess": 0.20, "p_slip": 0.15},
    "code": {"p_guess": 0.15, "p_slip": 0.08},
    "default": {"p_guess": DEFAULT_P_GUESS, "p_slip": DEFAULT_P_SLIP},
}

DIFFICULTY_MULTIPLIERS: dict[str, dict[str, float]] = {
    "easy": {"guess_mult": 1.3, "slip_mult": 0.7},
    "medium": {"guess_mult": 1.0, "slip_mult": 1.0},
    "hard": {"guess_mult": 0.7, "slip_mult": 1.3},
    "very_hard": {"guess_mult": 0.5, "slip_mult": 1.5},
}


def get_assessment_params(assessment_type: str | None) -> dict[str, float]:
    """Get BKT parameters based on assessment type."""
    if assessment_type is None:
        return ASSESSMENT_TYPE_PARAMS["default"]
    return ASSESSMENT_TYPE_PARAMS.get(assessment_type, ASSESSMENT_TYPE_PARAMS["default"])


def apply_difficulty_adjustment(
    base_p_guess: float, base_p_slip: float, difficulty: str | None
) -> tuple[float, float]:
    """Apply difficulty-based adjustments to p_guess and p_slip."""
    if difficulty is None or difficulty not in DIFFICULTY_MULTIPLIERS:
        return base_p_guess, base_p_slip
    mult = DIFFICULTY_MULTIPLIERS[difficulty]
    p_guess = max(0.01, min(0.99, base_p_guess * mult["guess_mult"]))
    p_slip = max(0.01, min(0.99, base_p_slip * mult["slip_mult"]))
    return p_guess, p_slip


def load_knowledge_units_from_path(path: Path) -> list[dict]:
    """Load knowledge unit definitions from JSON file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("knowledge_units", [])


def _timestamp() -> str:
    return f"{time.time():.6f}"


def _make_unit_record(unit_def: dict, domain: str, status: str) -> dict:
    """Build one per-unit state record with BKT fields."""
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
        "bkt_p_know": DEFAULT_P_KNOW_INIT,
        "bkt_p_slip": DEFAULT_P_SLIP,
        "bkt_p_guess": DEFAULT_P_GUESS,
        "bkt_p_transit": DEFAULT_P_TRANSIT,
        "last_practiced_at": _timestamp(),
    }


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
        # Reflection store for Reflect-Respond pipeline: facts and code the TA "believes"
        self._reflection_store: dict = {"facts": [], "code_implementations": []}

    def merge_persisted_state(
        self,
        units_state: dict[str, dict],
        reflection_store: dict | None = None,
    ) -> None:
        """Merge persisted units (e.g. from DB) into tracker; ensure BKT fields exist.
        If reflection_store is provided (e.g. from knowledge_state['reflection_store']), restore it.
        """
        if reflection_store is not None and isinstance(reflection_store, dict):
            self._reflection_store = {
                "facts": list(reflection_store.get("facts", [])),
                "code_implementations": list(reflection_store.get("code_implementations", [])),
            }
        for uid, rec in units_state.items():
            if uid not in self._state:
                continue
            self._state[uid] = dict(self._state[uid])
            self._state[uid].update(rec)
            r = self._state[uid]
            if "bkt_p_know" not in r:
                r["bkt_p_know"] = DEFAULT_P_KNOW_INIT
            if "bkt_p_slip" not in r:
                r["bkt_p_slip"] = DEFAULT_P_SLIP
            if "bkt_p_guess" not in r:
                r["bkt_p_guess"] = DEFAULT_P_GUESS
            if "bkt_p_transit" not in r:
                r["bkt_p_transit"] = DEFAULT_P_TRANSIT
            if "last_practiced_at" not in r:
                r["last_practiced_at"] = _timestamp()
            r["confidence"] = round(float(r.get("bkt_p_know", 0)), 4)

    def _get_prerequisites(self, unit_id: str) -> list[str]:
        """Return list of prerequisite unit IDs for this unit."""
        u = self._units.get(unit_id, {})
        return list(u.get("prerequisites", []) or [])

    def _parse_timestamp(self, ts: str) -> float:
        """Parse timestamp string to float seconds for decay calculation."""
        try:
            return float(ts)
        except (TypeError, ValueError):
            return time.time()

    def _days_since(self, ts: str) -> float:
        """Days since given timestamp (string)."""
        t = self._parse_timestamp(ts)
        return (time.time() - t) / 86400.0

    def _get_p_know_raw(self, unit_id: str) -> float:
        """Get raw p_know (no decay)."""
        rec = self._state.get(unit_id, {})
        return float(rec.get("bkt_p_know", DEFAULT_P_KNOW_INIT))

    def _effective_decay_lambda(self, unit_id: str) -> float:
        """Personalized decay: more teaching/testing evidence -> slower forgetting."""
        rec = self._state.get(unit_id, {})
        n_teaching = len(rec.get("teaching_evidence", []))
        n_testing = len(rec.get("testing_evidence", []))
        n_total = n_teaching + n_testing
        if n_total <= 0:
            return DECAY_LAMBDA
        return DECAY_LAMBDA / (1.0 + 0.15 * n_total)

    def get_p_know_decayed(self, unit_id: str) -> float:
        """Get p_know after applying Ebbinghaus-style decay (personalized by evidence count)."""
        rec = self._state.get(unit_id, {})
        p = float(rec.get("bkt_p_know", DEFAULT_P_KNOW_INIT))
        last = rec.get("last_practiced_at", _timestamp())
        days = self._days_since(last)
        if days <= 0:
            return p
        lam = self._effective_decay_lambda(unit_id)
        decay = math.exp(-lam * days)
        return p * decay

    def _prerequisites_satisfied(self, unit_id: str) -> bool:
        """True if all prerequisites have decayed p_know >= PREREQ_MIN_P_KNOW."""
        for prereq_id in self._get_prerequisites(unit_id):
            if self.get_p_know_decayed(prereq_id) < PREREQ_MIN_P_KNOW:
                return False
        return True

    def _decay_misconceptions_after_teaching(
        self,
        unit_id: str,
        *,
        decay_factor: float = 0.85,
        drop_threshold: float = 0.2,
    ) -> None:
        """After teaching, reduce severity of active misconceptions on this unit; remove if below threshold."""
        if unit_id not in self._state:
            return
        rec = self._state[unit_id]
        active = rec.get("active_misconceptions", [])
        new_active = []
        for m in active:
            sev = float(m.get("severity_score", 0.5))
            sev = sev * decay_factor
            if sev >= drop_threshold:
                m["severity_score"] = round(sev, 3)
                new_active.append(m)
        rec["active_misconceptions"] = new_active
        if new_active != active:
            rec["last_updated"] = _timestamp()
            self._last_updated = rec["last_updated"]

    def _effective_p_transit(self, unit_id: str) -> float:
        """p_transit reduced to 0 if prerequisites not satisfied."""
        if not self._prerequisites_satisfied(unit_id):
            return 0.0
        rec = self._state.get(unit_id, {})
        return float(rec.get("bkt_p_transit", DEFAULT_P_TRANSIT))

    def update_bkt_after_observation(
        self,
        unit_ids: list[str],
        correct: bool,
        timestamp: str | None = None,
        *,
        assessment_type: str | None = None,
        difficulty: str | None = None,
    ) -> None:
        """
        Update BKT parameters after a test observation (correct/incorrect).
        For each unit in unit_ids: apply Bayes update on p_know, then if correct apply transit.

        Args:
            unit_ids: List of knowledge unit IDs to update
            correct: Whether the observation was correct
            timestamp: Optional timestamp for the observation
            assessment_type: Optional assessment type for M-10 (e.g., 'parsons', 'dropdown')
            difficulty: Optional difficulty level for M-13 (e.g., 'easy', 'medium', 'hard')
        """
        now = timestamp or _timestamp()

        # M-10: Get assessment-type-specific base parameters
        base_params = get_assessment_params(assessment_type)

        for uid in unit_ids:
            if uid not in self._state:
                continue
            rec = self._state[uid]
            p_know = float(rec.get("bkt_p_know", DEFAULT_P_KNOW_INIT))

            # M-10 & M-13: Apply assessment type and difficulty adjustments
            base_p_guess = float(rec.get("bkt_p_guess", base_params["p_guess"]))
            base_p_slip = float(rec.get("bkt_p_slip", base_params["p_slip"]))
            p_guess, p_slip = apply_difficulty_adjustment(
                base_p_guess, base_p_slip, difficulty
            )

            p_transit = self._effective_p_transit(uid)

            if correct:
                p_correct = p_know * (1 - p_slip) + (1 - p_know) * p_guess
                if p_correct <= 0:
                    p_correct = 1e-6
                p_know_given_correct = (p_know * (1 - p_slip)) / p_correct
                p_know = p_know_given_correct + (1 - p_know_given_correct) * p_transit
            else:
                p_incorrect = p_know * p_slip + (1 - p_know) * (1 - p_guess)
                if p_incorrect <= 0:
                    p_incorrect = 1e-6
                p_know = (p_know * p_slip) / p_incorrect

            p_know = max(0.01, min(0.99, p_know))
            rec["bkt_p_know"] = p_know
            rec["last_practiced_at"] = now
            rec["last_updated"] = now
            rec["confidence"] = round(p_know, 4)

            # Store the effective parameters used for this observation
            rec["last_p_guess_used"] = p_guess
            rec["last_p_slip_used"] = p_slip
            rec["last_assessment_type"] = assessment_type
            rec["last_difficulty"] = difficulty

            self._sync_status_from_bkt(uid)
        self._last_updated = now

    def _sync_status_from_bkt(self, unit_id: str) -> None:
        """Set status from BKT p_know and active_misconceptions (do not override misconception/corrected)."""
        if unit_id not in self._state:
            return
        rec = self._state[unit_id]
        if rec.get("status") == self.STATUS_MISCONCEPTION or rec.get("status") == self.STATUS_CORRECTED:
            return
        p = float(rec.get("bkt_p_know", 0))
        if p >= THRESHOLD_LEARNED:
            rec["status"] = self.STATUS_LEARNED
        elif p >= THRESHOLD_PARTIALLY_LEARNED:
            rec["status"] = self.STATUS_PARTIALLY_LEARNED
        else:
            rec["status"] = self.STATUS_UNKNOWN

    def get_domain(self) -> str:
        return self._domain

    def get_schema_version(self) -> str:
        return self._schema_version

    def get_state(self) -> dict[str, str]:
        """Legacy view: unit_id -> status (status kept in sync with BKT)."""
        return {uid: rec["status"] for uid, rec in self._state.items()}

    def get_full_state(self) -> dict:
        self._last_updated = _timestamp()
        return {
            "domain": self._domain,
            "schema_version": self._schema_version,
            "last_updated": self._last_updated,
            "units": dict(self._state),
            "reflection_store": dict(self._reflection_store),
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
        affected_units: list[str] | None = None,
    ) -> bool:
        if unit_id not in self._state:
            return False
        rec = self._state[unit_id]
        for m in rec.get("active_misconceptions", []):
            if m.get("misconception_id") == misconception_id:
                m["trigger_count"] = m.get("trigger_count", 1) + 1
                m["severity_score"] = min(1.0, 0.3 + 0.1 * m["trigger_count"])
                rec["last_updated"] = _timestamp()
                self._last_updated = rec["last_updated"]
                return False
        now = _timestamp()
        rec["active_misconceptions"].append({
            "misconception_id": misconception_id,
            "activated_at": now,
            "trigger": trigger,
            "trigger_reference": trigger_reference,
            "flagged_for_correction": False,
            "trigger_count": 1,
            "severity_score": 0.4,
        })
        rec["last_updated"] = now
        self._last_updated = now
        if set_status_to_misconception:
            rec["status"] = self.STATUS_MISCONCEPTION
        if affected_units:
            for uid in affected_units:
                if uid in self._state and uid != unit_id:
                    r = self._state[uid]
                    p = float(r.get("bkt_p_know", 0.5))
                    r["bkt_p_know"] = max(0.01, p - 0.2)
                    r["last_updated"] = now
                    self._sync_status_from_bkt(uid)
        return True

    def _bkt_update_after_teaching_observation(
        self,
        uid: str,
        quality_score: float,
        now: str,
    ) -> None:
        """
        Apply standard BKT update for a teaching observation (treat as correct observation).
        p_transit is scaled by quality_score so higher-quality teaching increases transition probability.
        """
        if uid not in self._state:
            return
        rec = self._state[uid]
        p_know = float(rec.get("bkt_p_know", DEFAULT_P_KNOW_INIT))
        p_slip = float(rec.get("bkt_p_slip", DEFAULT_P_SLIP))
        p_guess = float(rec.get("bkt_p_guess", DEFAULT_P_GUESS))
        p_transit = self._effective_p_transit(uid)
        # Scale p_transit by teaching quality (0.5--1.0) so good teaching increases chance of learning
        quality = max(0.3, min(1.0, float(quality_score)))
        p_transit = p_transit * (0.5 + 0.5 * quality)
        # BKT update given "correct" observation (student taught correctly)
        p_correct = p_know * (1 - p_slip) + (1 - p_know) * p_guess
        if p_correct <= 0:
            p_correct = 1e-6
        p_know_given_correct = (p_know * (1 - p_slip)) / p_correct
        p_know = p_know_given_correct + (1 - p_know_given_correct) * p_transit
        p_know = max(0.01, min(0.99, p_know))
        rec["bkt_p_know"] = p_know
        rec["last_practiced_at"] = now
        rec["last_updated"] = now
        rec["confidence"] = round(p_know, 4)
        self._sync_status_from_bkt(uid)

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
        quality_score = float(teaching_event.get("quality_score", 0.7)) if teaching_event else 0.7
        now = _timestamp()
        self._last_updated = now
        for uid in unit_ids:
            if uid not in self._state:
                continue
            rec = self._state[uid]
            state_before = rec["status"]
            if not self._prerequisites_satisfied(uid):
                new_status_here = self.STATUS_PARTIALLY_LEARNED
                rec["bkt_p_know"] = min(0.6, float(rec.get("bkt_p_know", 0)) + 0.2)
            else:
                new_status_here = new_status
                self._bkt_update_after_teaching_observation(uid, quality_score, now)
                new_status_here = rec["status"]
            rec["last_practiced_at"] = now
            rec["last_updated"] = now
            rec["confidence"] = round(rec.get("bkt_p_know", 0), 4)
            if event_id is not None:
                rec["teaching_evidence"].append({
                    "teaching_event_id": event_id,
                    "timestamp": now,
                    "topic_taught": topic,
                    "knowledge_units_taught": list(units_taught),
                    "state_before": state_before,
                    "state_after": new_status_here,
                    "misconception_activated": None,
                    "note": note,
                })
            # Confidence decay: correct teaching weakens active misconceptions on this unit
            self._decay_misconceptions_after_teaching(uid, decay_factor=0.85, drop_threshold=0.2)

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

    def get_bkt_state(self) -> dict[str, float]:
        """Return decayed p_know per unit (for API / analytics)."""
        return {uid: round(self.get_p_know_decayed(uid), 4) for uid in self._state}

    def get_reflection_store(self) -> dict:
        """Return the reflection store (facts, code_implementations) for Reflect-Respond pipeline."""
        return dict(self._reflection_store)

    def set_reflection_store(self, store: dict) -> None:
        """Set the reflection store (e.g. after Reflect-Respond pipeline update)."""
        self._reflection_store = {
            "facts": list(store.get("facts", [])),
            "code_implementations": list(store.get("code_implementations", [])),
        }

    # Mapping from Assessment Studio concept labels to TA KU ids
    _CONCEPT_TO_KU_MAP: dict[str, list[str]] = {
        "variables": ["variable_assignment"],
        "arithmetic operators": ["arithmetic_operators"],
        "comparison operators": ["comparison_operators"],
        "logical operators": ["logical_operators"],
        "selection statements (if/else, etc.)": ["if_else"],
        "if/else": ["if_else"],
        "loops": ["for_loop_range", "while_loop"],
        "for loops": ["for_loop_range"],
        "while loops": ["while_loop"],
        "lists": ["list_basics", "list_indexing"],
        "strings": ["string_basics", "string_methods"],
        "dictionaries": ["variable_assignment"],
        "functions": ["function_def", "function_params", "return_statement"],
        "input/output": ["print_function", "user_input"],
        "type conversion": ["type_conversion"],
    }

    def _resolve_concepts_to_ku_ids(self, concepts: list[str]) -> list[str]:
        """Map assessment concept labels to KU ids present in this tracker."""
        ku_ids: list[str] = []
        seen: set[str] = set()
        for concept in concepts:
            key = concept.strip().lower()
            mapped = self._CONCEPT_TO_KU_MAP.get(key, [])
            for ku_id in mapped:
                if ku_id in self._state and ku_id not in seen:
                    ku_ids.append(ku_id)
                    seen.add(ku_id)
        return ku_ids

    def update_from_assessment(
        self,
        concepts: list[str],
        correct: bool,
        *,
        timestamp: str | None = None,
    ) -> list[str]:
        """
        Update BKT state after a structured assessment attempt.
        Maps concept labels from the assessment to KU ids and applies
        a standard BKT observation update.
        Returns the list of KU ids that were updated.
        """
        ku_ids = self._resolve_concepts_to_ku_ids(concepts)
        if not ku_ids:
            return []
        self.update_bkt_after_observation(ku_ids, correct, timestamp)
        now = timestamp or _timestamp()
        for uid in ku_ids:
            if uid in self._state:
                self._state[uid].setdefault("assessment_evidence", [])
                self._state[uid]["assessment_evidence"].append({
                    "timestamp": now,
                    "correct": correct,
                    "concepts": concepts,
                })
        return ku_ids
