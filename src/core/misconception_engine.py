"""
Misconception engine: activate, correct (unlearn), relearn, and auto-detect from failed attempts.
Uses trace layer for recording events.
"""

import re
import uuid
from typing import Any

from src.core.trace import (
    record_misconception_activation,
    record_correction_event,
    record_relearning_event,
)


def _pattern_match_misconception(ta_code: str, misconception: dict) -> float:
    """
    Return a confidence score in [0, 1] that ta_code exhibits this misconception.
    Uses simple pattern checks against example_incorrect_code and description.
    """
    code = (ta_code or "").strip()
    if not code:
        return 0.0
    mid = misconception.get("id", "")
    incorrect_ex = (misconception.get("example_incorrect_code") or "").strip()
    desc = (misconception.get("description") or "").lower()
    score = 0.0
    if "assign_vs_equal" in mid or "comparison_in_if" in mid:
        if re.search(r"if\s+[^=]+=\s*[^=]", code) or "if " in code and " = " in code and " == " not in code:
            score = 0.8
    if "off_by_one_range" in mid:
        if "range(" in code and ("+ 1" in code or "i + 1" in code or "i+1" in code):
            score = 0.75
    if "string_int_concat" in mid:
        if re.search(r'["\'][^"\']*["\']\s*\+\s*\d+', code) or " + 20" in code or " + 1" in code:
            score = 0.8
    if "indent_error" in mid:
        if "if " in code or "for " in code or "while " in code:
            lines = code.split("\n")
            for i, line in enumerate(lines):
                if line.strip().startswith(("if ", "for ", "while ")) and i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line and not next_line.startswith(" ") and not next_line.startswith("\t"):
                        score = 0.85
                    break
    if "list_index_one_based" in mid:
        if "nums[1]" in code or "[1]" in code and "range(1" not in code:
            score = 0.7
    if incorrect_ex and score == 0.0:
        if incorrect_ex[:30] in code or incorrect_ex.replace(" ", "")[:20] in code.replace(" ", ""):
            score = 0.6
    return score


def infer_misconception_from_failed_attempt(
    ta_code: str,
    problem: dict,
    misconceptions_catalog: list[dict],
    *,
    min_confidence: float = 0.6,
) -> list[tuple[str, str, float]]:
    """
    Infer likely (misconception_id, unit_id, confidence) from failed TA code.
    problem may contain knowledge_units_tested to prefer units related to the task.
    """
    units_tested = set(problem.get("knowledge_units_tested", []) or [])
    out: list[tuple[str, str, float]] = []
    for m in misconceptions_catalog:
        mid = m.get("id", "")
        affected = m.get("affected_knowledge_units", []) or []
        conf = _pattern_match_misconception(ta_code, m)
        if conf < min_confidence:
            continue
        for uid in affected:
            if not units_tested or uid in units_tested:
                out.append((mid, uid, conf))
                break
        else:
            if affected:
                out.append((mid, affected[0], conf))
    out.sort(key=lambda x: -x[2])
    return out[:3]


def try_auto_activate_misconception_after_fail(
    tracker: Any,
    problem: dict,
    ta_code: str,
    misconceptions_catalog: list[dict],
    *,
    use_llm_diagnosis: bool = True,
) -> bool:
    """
    After a failed attempt, infer misconceptions (LLM-assisted or pattern-based) and activate the best match if not already active.
    Returns True if at least one was activated.
    """
    inferred: list[tuple[str, str, float]] = []
    if use_llm_diagnosis:
        try:
            from src.core.misconception_diagnosis import diagnose_from_failed_attempt
            inferred = diagnose_from_failed_attempt(
                ta_code,
                problem,
                misconceptions_catalog,
                use_llm=True,
                fallback_to_pattern=True,
            )
        except Exception:
            inferred = []
    if not inferred:
        inferred = infer_misconception_from_failed_attempt(
            ta_code, problem, misconceptions_catalog, min_confidence=0.6
        )
    any_activated = False
    for misconception_id, unit_id, _ in inferred:
        if unit_id not in tracker.get_unit_ids():
            continue
        active_ids = tracker.get_active_misconception_ids({unit_id})
        if misconception_id in active_ids:
            continue
        m = next((x for x in misconceptions_catalog if x.get("id") == misconception_id), None)
        affected = (m.get("affected_knowledge_units", []) or []) if m else []
        added = tracker.activate_misconception(
            unit_id,
            misconception_id,
            trigger="auto_from_failed_attempt",
            trigger_reference=problem.get("problem_id", ""),
            set_status_to_misconception=False,
            affected_units=affected,
        )
        if added:
            state_before = tracker.get_state().get(unit_id, "unknown")
            state_after = tracker.get_state().get(unit_id, "unknown")
            rec = tracker.get_unit_record(unit_id) if hasattr(tracker, "get_unit_record") else {}
            sev = count = None
            for am in rec.get("active_misconceptions", []):
                if am.get("misconception_id") == misconception_id:
                    sev = am.get("severity_score")
                    count = am.get("trigger_count")
                    break
            record_misconception_activation(
                domain=tracker.get_domain(),
                unit_id=unit_id,
                misconception_id=misconception_id,
                trigger="auto_from_failed_attempt",
                trigger_reference=problem.get("problem_id", ""),
                state_before=state_before,
                state_after=state_after,
                severity_score=sev,
                trigger_count=count,
            )
            any_activated = True
    return any_activated


def activate_misconception_for_unit(
    tracker,
    unit_id: str,
    misconception_id: str,
    trigger: str = "pre_seeded",
    trigger_reference: str | None = None,
    *,
    affected_units_from_catalog: list[str] | None = None,
) -> bool:
    """Activate a misconception for the given unit. Records trace event. Optionally propagate to affected KUs."""
    if unit_id not in tracker.get_unit_ids():
        return False
    state_before = tracker.get_state().get(unit_id, "unknown")
    affected = affected_units_from_catalog
    added = tracker.activate_misconception(
        unit_id,
        misconception_id,
        trigger=trigger,
        trigger_reference=trigger_reference,
        set_status_to_misconception=False,
        affected_units=affected,
    )
    if not added:
        return False
    state_after = tracker.get_state().get(unit_id, "unknown")
    rec = tracker.get_unit_record(unit_id) if hasattr(tracker, "get_unit_record") else {}
    sev = count = None
    for am in rec.get("active_misconceptions", []):
        if am.get("misconception_id") == misconception_id:
            sev = am.get("severity_score")
            count = am.get("trigger_count")
            break
    record_misconception_activation(
        domain=tracker.get_domain(),
        unit_id=unit_id,
        misconception_id=misconception_id,
        trigger=trigger,
        trigger_reference=trigger_reference,
        state_before=state_before,
        state_after=state_after,
        severity_score=sev,
        trigger_count=count,
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


def get_adaptive_remediation_hint(
    misconception_catalog_entry: dict,
    severity_score: float | None = None,
    trigger_count: int | None = None,
) -> str:
    """
    Return remediation hint, optionally appending advice when severity or trigger count is high.
    """
    base = (misconception_catalog_entry.get("remediation_hint") or "").strip()
    if not base:
        return base
    if (severity_score is not None and severity_score >= 0.6) or (trigger_count is not None and trigger_count >= 2):
        return base + " (This misconception has appeared multiple times; consider re-teaching with a concrete example.)"
    return base


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
