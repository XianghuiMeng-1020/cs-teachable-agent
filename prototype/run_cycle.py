"""
Stage F: Shared-cycle orchestration (Interaction Engine path).

Single entry point for one teaching–testing cycle per SHARED_CORE_ARCHITECTURE §14:
  teaching input → state update → dialogue → task selection → TA attempt → evaluation → mastery/trace.

Engines are called in order; trace is written at each step. Scenarios configure inputs
and call these functions instead of manually wiring components.
"""

from __future__ import annotations

import uuid
from typing import Any

from state_tracker import StateTracker
from teaching_events import make_teaching_event, apply_teaching_event
from problem_selector import (
    load_problems,
    select_problem,
    get_eligible_problem_ids,
    get_ineligible_reasons,
)
from ta_conversation import get_ta_learner_response
from ta_code_generation import get_ta_code_attempt
from mastery_evaluator import (
    evaluate_attempt,
    mastery_summary,
    build_mastery_report,
    record_attempt_to_state,
)
from trace_history import (
    record_teaching_event,
    record_knowledge_state_update,
    record_learner_dialogue,
    record_task_selection,
    record_ta_attempt,
    record_evaluation_result,
    record_mastery_update,
)
from misconception_engine import activate_misconception_for_unit
from correction_events import make_correction_event


def _use_llm_code() -> bool:
    """True if env USE_LLM_CODE is set to 1 or true."""
    import os
    v = os.environ.get("USE_LLM_CODE", "").strip().lower()
    return v in ("1", "true")


def run_teaching_and_test(
    tracker: StateTracker,
    problems: list[dict],
    teaching_event: dict,
    *,
    run_attempt: bool = True,
    activate_misconception: dict[str, Any] | None = None,
    use_llm_code: bool | None = None,
) -> dict[str, Any]:
    """
    One full teaching–testing cycle: apply teaching → state update → dialogue →
    task selection → (optional) attempt → evaluation → mastery/trace.

    - tracker: Knowledge State Engine (single source of truth).
    - problems: task bank from domain (e.g. load_problems(problems_path)).
    - teaching_event: from make_teaching_event(...).
    - run_attempt: if True and a task is selected, run TA attempt + evaluation + mastery/trace.
    - activate_misconception: optional {unit_id, misconception_id, trigger, trigger_reference}
      to activate a misconception after teaching (e.g. for Scenario C/D).
    - use_llm_code: if None, use env USE_LLM_CODE; if False, stub only; if True, try LLM.

    Returns a result dict for scenario output (teaching_event, learned_units, ta_learner_response,
    selected_problem, ta_code, attempt_result, mastery_summary, mastery_report, pass_fail, etc.).
    """
    domain = tracker.get_domain()
    use_llm = use_llm_code if use_llm_code is not None else _use_llm_code()

    # 1) Teaching event → trace
    record_teaching_event(
        domain=domain,
        topic_taught=teaching_event.get("topic_taught", ""),
        knowledge_units_taught=teaching_event.get("knowledge_units_taught", []),
        note=teaching_event.get("note", ""),
        teaching_event_id=teaching_event.get("teaching_event_id"),
    )

    # 2) State update (Knowledge State Engine)
    unit_ids = teaching_event.get("knowledge_units_taught", [])
    state_before = {uid: tracker.get_state().get(uid, "unknown") for uid in unit_ids}
    apply_teaching_event(tracker, teaching_event)
    state_after = {uid: "learned" for uid in unit_ids}
    record_knowledge_state_update(
        domain=domain,
        trigger=teaching_event.get("teaching_event_id", "teaching"),
        unit_ids=unit_ids,
        state_before=state_before,
        state_after=state_after,
        evidence_source=teaching_event.get("teaching_event_id"),
    )

    # 3) Optional misconception activation (Misconception Engine)
    if activate_misconception:
        activate_misconception_for_unit(
            tracker,
            unit_id=activate_misconception["unit_id"],
            misconception_id=activate_misconception["misconception_id"],
            trigger=activate_misconception.get("trigger", "scenario"),
            trigger_reference=activate_misconception.get("trigger_reference") or teaching_event.get("teaching_event_id"),
        )

    # 4) Learner Dialogue Engine
    learned = tracker.get_learned_units()
    active_mis_ids = tracker.get_active_misconception_ids(learned)
    ta_learner_response = get_ta_learner_response(
        learned, teaching_event, active_misconceptions=active_mis_ids or None
    )
    record_learner_dialogue(
        domain=domain,
        teaching_event_id=teaching_event.get("teaching_event_id", ""),
        learned_unit_ids=sorted(learned),
        response_text=ta_learner_response,
        active_misconception_ids=active_mis_ids,
    )

    # 5) Task Engine: selection
    eligible_ids = get_eligible_problem_ids(problems, learned)
    ineligible = get_ineligible_reasons(problems, learned)
    selected = select_problem(problems, learned)
    record_task_selection(
        domain=domain,
        eligible_unit_ids=sorted(learned),
        selected_task_id=selected.get("problem_id") if selected else None,
        eligible_task_ids=eligible_ids,
        ineligible_reasons=ineligible[:10],
    )

    # 6) TA Attempt Engine + Mastery Evaluator (if run_attempt and task selected)
    ta_code = ""
    result = None
    summary = None
    attempt_id = str(uuid.uuid4()) if selected else None
    units_tested = set(selected.get("knowledge_units_tested", [])) if selected else set()
    active_mis_for_attempt = list(tracker.get_active_misconception_ids(units_tested)) if selected else []

    if run_attempt and selected:
        ta_code = get_ta_code_attempt(
            selected,
            learned,
            active_misconceptions=active_mis_for_attempt or None,
            force_fail_problem_ids=None,
            use_llm_code=use_llm,
        )
        if ta_code:
            record_ta_attempt(
                domain=domain,
                task_id=selected.get("problem_id", ""),
                attempt_id=attempt_id,
                learned_unit_ids=sorted(learned),
                output_summary=(ta_code[:200] + "..." if len(ta_code) > 200 else ta_code),
                guard_passed=True,
                fallback_used=not use_llm,
                active_misconception_ids=active_mis_for_attempt,
            )
        result = evaluate_attempt(selected, ta_code) if ta_code else None
        summary = mastery_summary(selected, result, []) if result else None
        if result:
            mis_per_unit = {}
            if active_mis_for_attempt:
                for uid in selected.get("knowledge_units_tested", []):
                    mis_per_unit[uid] = active_mis_for_attempt[0]
            record_attempt_to_state(
                tracker,
                selected,
                result,
                attempt_id,
                misconception_active_per_unit=mis_per_unit or None,
                period="during_misconception" if active_mis_for_attempt else "before_misconception",
            )
            record_evaluation_result(
                domain=domain,
                task_id=selected.get("problem_id", ""),
                attempt_id=attempt_id,
                pass_fail=result.get("passed", False),
                unit_ids_tested=selected.get("knowledge_units_tested", []),
                mastery_level_before=None,
                mastery_level_after=summary.get("overall_level") if summary else None,
                misconception_active_during_attempt=active_mis_for_attempt[0] if active_mis_for_attempt else None,
            )
            for uid in selected.get("knowledge_units_tested", []):
                record_mastery_update(
                    domain=domain,
                    unit_id=uid,
                    mastery_level=summary.get("level_per_unit", {}).get(uid, "not_assessed") if summary else "not_assessed",
                    pass_rate=summary.get("per_unit_pass_rate", {}).get(uid) if summary else None,
                    attempt_count=1,
                    trigger=attempt_id,
                )

    report = build_mastery_report(
        selected, learned, result, summary, ta_code
    ) if selected else build_mastery_report(None, learned, None, None)

    return {
        "teaching_event": teaching_event,
        "learned_units": sorted(learned),
        "ta_learner_response": ta_learner_response,
        "eligible_problem_ids": eligible_ids,
        "ineligible_reasons": ineligible[:5],
        "selected_problem": selected,
        "problem_attempted": run_attempt and selected is not None,
        "ta_code": ta_code,
        "attempt_result": result,
        "mastery_summary": summary,
        "mastery_report": report,
        "pass_fail": result.get("passed") if result else None,
        "active_misconception_ids": active_mis_for_attempt,
    }


def run_correction(
    tracker: StateTracker,
    unit_id: str,
    misconception_id: str,
    trigger: str = "explicit_correction_event",
    teaching_event_id: str | None = None,
    correction_event_id: str | None = None,
) -> tuple[bool, dict]:
    """
    Apply correction (unlearning) for a unit. Uses Misconception Engine; writes trace.
    Returns (applied: bool, correction_event: dict).
    """
    from misconception_engine import apply_correction

    correction_event = make_correction_event(
        unit_id=unit_id,
        misconception_id=misconception_id,
        trigger=trigger,
        teaching_event_id=teaching_event_id,
        correction_event_id=correction_event_id,
    )
    domain = tracker.get_domain()
    state_before_correct = tracker.get_state().get(unit_id, "unknown")
    applied = apply_correction(
        tracker,
        unit_id=unit_id,
        misconception_id=misconception_id,
        trigger=correction_event["trigger"],
        teaching_event_id=correction_event.get("teaching_event_id"),
        correction_event_id=correction_event.get("correction_event_id"),
    )
    state_after_correct = tracker.get_state().get(unit_id, "unknown")
    if applied:
        record_knowledge_state_update(
            domain=domain,
            trigger=correction_event.get("correction_event_id", "correction"),
            unit_ids=[unit_id],
            state_before=state_before_correct,
            state_after=state_after_correct,
            evidence_source=correction_event.get("correction_event_id"),
        )
    return applied, correction_event


def run_relearning_step(
    tracker: StateTracker,
    teaching_event: dict,
) -> dict[str, Any]:
    """
    Add relearning evidence from a follow-up teaching event (no full cycle).
    Records teaching_event and state update in trace.
    Returns dict with state_after_relearn, learned_units.
    """
    from misconception_engine import add_relearning_evidence_from_teaching

    domain = tracker.get_domain()
    record_teaching_event(
        domain=domain,
        topic_taught=teaching_event.get("topic_taught", ""),
        knowledge_units_taught=teaching_event.get("knowledge_units_taught", []),
        note=teaching_event.get("note", ""),
        teaching_event_id=teaching_event.get("teaching_event_id"),
    )
    unit_id = teaching_event.get("knowledge_units_taught", [None])[0]
    if not unit_id:
        return {"state_after_relearn": {}, "learned_units": sorted(tracker.get_learned_units())}
    state_before = tracker.get_state().get(unit_id, "unknown")
    add_relearning_evidence_from_teaching(
        tracker,
        unit_id=unit_id,
        teaching_event_id=teaching_event["teaching_event_id"],
    )
    state_after = tracker.get_state().get(unit_id, "unknown")
    learned = tracker.get_learned_units()
    record_knowledge_state_update(
        domain=domain,
        trigger=teaching_event.get("teaching_event_id", "relearning"),
        unit_ids=[unit_id],
        state_before=state_before,
        state_after=state_after,
        evidence_source=teaching_event.get("teaching_event_id"),
    )
    return {
        "state_after_relearn": state_after,
        "learned_units": sorted(learned),
    }


def run_test_only(
    tracker: StateTracker,
    problems: list[dict],
    *,
    use_llm_code: bool | None = None,
) -> dict[str, Any]:
    """
    Run only task selection → attempt → evaluation (no teaching). Used e.g. for
    second attempt after relearning in Scenario D.
    """
    domain = tracker.get_domain()
    use_llm = use_llm_code if use_llm_code is not None else _use_llm_code()
    learned = tracker.get_learned_units()
    eligible_ids = get_eligible_problem_ids(problems, learned)
    ineligible = get_ineligible_reasons(problems, learned)
    selected = select_problem(problems, learned)
    record_task_selection(
        domain=domain,
        eligible_unit_ids=sorted(learned),
        selected_task_id=selected.get("problem_id") if selected else None,
        eligible_task_ids=eligible_ids,
        ineligible_reasons=ineligible[:10],
    )

    ta_code = ""
    result = None
    summary = None
    attempt_id = str(uuid.uuid4()) if selected else None
    if selected:
        ta_code = get_ta_code_attempt(
            selected,
            learned,
            active_misconceptions=None,
            force_fail_problem_ids=None,
            use_llm_code=use_llm,
        )
        if ta_code:
            record_ta_attempt(
                domain=domain,
                task_id=selected.get("problem_id", ""),
                attempt_id=attempt_id,
                learned_unit_ids=sorted(learned),
                output_summary=(ta_code[:200] + "..." if len(ta_code) > 200 else ta_code),
                guard_passed=True,
                fallback_used=not use_llm,
                active_misconception_ids=[],
            )
        result = evaluate_attempt(selected, ta_code) if ta_code else None
        summary = mastery_summary(selected, result, []) if result else None
        if result:
            record_attempt_to_state(
                tracker,
                selected,
                result,
                attempt_id,
                period="after_correction",
            )
            record_evaluation_result(
                domain=domain,
                task_id=selected.get("problem_id", ""),
                attempt_id=attempt_id,
                pass_fail=result.get("passed", False),
                unit_ids_tested=selected.get("knowledge_units_tested", []),
                mastery_level_after=summary.get("overall_level") if summary else None,
                misconception_active_during_attempt=None,
            )
            for uid in selected.get("knowledge_units_tested", []):
                record_mastery_update(
                    domain=domain,
                    unit_id=uid,
                    mastery_level=summary.get("level_per_unit", {}).get(uid, "not_assessed") if summary else "not_assessed",
                    pass_rate=summary.get("per_unit_pass_rate", {}).get(uid) if summary else None,
                    attempt_count=2,
                    trigger=attempt_id,
                )

    report = build_mastery_report(
        selected, learned, result, summary, ta_code
    ) if selected else build_mastery_report(None, learned, None, None)

    return {
        "selected_problem": selected,
        "ta_code": ta_code,
        "attempt_result": result,
        "mastery_summary": summary,
        "mastery_report": report,
        "pass_fail": result.get("passed") if result else None,
        "learned_units": sorted(learned),
    }
