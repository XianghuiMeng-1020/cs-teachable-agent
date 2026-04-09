"""
Shared-cycle orchestration: teaching input -> state update -> dialogue -> task selection
-> TA attempt -> evaluation -> mastery/trace.
"""

from __future__ import annotations

import os
import uuid
from typing import Any

from src.core.knowledge_state import StateTracker
from src.core.teaching_events import make_teaching_event, apply_teaching_event
from src.core.task_engine import (
    load_problems,
    select_problem,
    get_eligible_problem_ids,
    get_ineligible_reasons,
)
from src.core.dialogue_engine import get_ta_learner_response
from src.core.reflect_respond import run_reflect_respond_pipeline
from src.core.mode_shifting import maybe_append_questioner_response
from src.core.attempt_engine import get_ta_code_attempt
from src.core.evaluator import (
    evaluate_attempt as _evaluate_attempt_python,
    mastery_summary,
    build_mastery_report,
    record_attempt_to_state,
)
from src.core.trace import (
    record_teaching_event,
    record_knowledge_state_update,
    record_learner_dialogue,
    record_task_selection,
    record_ta_attempt,
    record_evaluation_result,
    record_mastery_update,
)
from src.core.misconception_engine import activate_misconception_for_unit
from src.core.correction_events import make_correction_event
from src.core.misconception_diagnosis import diagnose_from_teaching


def _use_llm_code() -> bool:
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
    domain_adapter: Any = None,
    conversation_history: list[dict] | None = None,
) -> dict[str, Any]:
    """
    One full teaching–testing cycle. If domain_adapter is provided, use it to get
    filled prompts for dialogue and code generation; otherwise use stubs.
    """
    domain = tracker.get_domain()
    use_llm = use_llm_code if use_llm_code is not None else _use_llm_code()

    record_teaching_event(
        domain=domain,
        topic_taught=teaching_event.get("topic_taught", ""),
        knowledge_units_taught=teaching_event.get("knowledge_units_taught", []),
        note=teaching_event.get("note", ""),
        teaching_event_id=teaching_event.get("teaching_event_id"),
    )

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

    if activate_misconception:
        activate_misconception_for_unit(
            tracker,
            unit_id=activate_misconception["unit_id"],
            misconception_id=activate_misconception["misconception_id"],
            trigger=activate_misconception.get("trigger", "scenario"),
            trigger_reference=activate_misconception.get("trigger_reference")
            or teaching_event.get("teaching_event_id"),
        )

    if domain_adapter and teaching_event.get("note"):
        try:
            catalog = domain_adapter.load_misconceptions()
            unit_ids = list(tracker.get_unit_ids())
            diag = diagnose_from_teaching(
                teaching_event.get("note", ""),
                unit_ids,
                catalog,
                use_llm=True,
            )
            if (
                diag.get("interpretation") == "incorrect"
                and diag.get("misconception_id")
                and diag.get("confidence", 0) >= 0.6
            ):
                for uid in (diag.get("affected_unit_ids") or [])[:3]:
                    if uid in tracker.get_unit_ids():
                        activate_misconception_for_unit(
                            tracker,
                            uid,
                            diag["misconception_id"],
                            trigger="llm_diagnosis_from_teaching",
                            trigger_reference=teaching_event.get("teaching_event_id"),
                        )
                        break
        except Exception:
            pass

    learned = tracker.get_learned_units()
    active_mis_ids = tracker.get_active_misconception_ids(learned)
    ta_learner_response: str
    # Prefer Reflect-Respond pipeline when domain adapter is present (knowledge-state-constrained response)
    if domain_adapter is not None:
        reflection_store = tracker.get_reflection_store()
        ta_learner_response, updated_store = run_reflect_respond_pipeline(
            reflection_store,
            teaching_event,
            list(learned),
            active_mis_ids or [],
            tracker.get_domain(),
            conversation_history=conversation_history,
            student_input=teaching_event.get("note"),
            use_llm=True,
        )
        tracker.set_reflection_store(updated_store)
        # Mode-shifting: every 3 turns append a thought-provoking "why"/"how" question
        msg_count = (len(conversation_history) + 1) if conversation_history else 1
        ta_learner_response = maybe_append_questioner_response(
            ta_learner_response,
            msg_count,
            teaching_event.get("topic_taught", ""),
            teaching_event.get("note", ""),
            tracker.get_domain(),
            list(learned),
            active_mis_ids,
            conversation_history,
            phase="teach",
        )
    else:
        filled_dialogue_prompt = None
        if domain_adapter and hasattr(domain_adapter, "get_conversation_prompt"):
            filled_dialogue_prompt = domain_adapter.get_conversation_prompt(
                tracker.get_full_state(), teaching_event, list(learned)
            )
        ta_learner_response = get_ta_learner_response(
            learned,
            teaching_event,
            active_misconceptions=active_mis_ids or None,
            filled_prompt=filled_dialogue_prompt,
            use_llm=True if filled_dialogue_prompt else None,
            conversation_history=conversation_history,
        )
        if conversation_history is not None:
            msg_count = len(conversation_history) + 1
            ta_learner_response = maybe_append_questioner_response(
                ta_learner_response,
                msg_count,
                teaching_event.get("topic_taught", ""),
                teaching_event.get("note", ""),
                tracker.get_domain(),
                list(learned),
                active_mis_ids,
                conversation_history,
                phase="teach",
            )
    record_learner_dialogue(
        domain=domain,
        teaching_event_id=teaching_event.get("teaching_event_id", ""),
        learned_unit_ids=sorted(learned),
        response_text=ta_learner_response,
        active_misconception_ids=active_mis_ids,
    )

    eligible_ids = get_eligible_problem_ids(problems, learned)
    ineligible = get_ineligible_reasons(problems, learned)
    selected = select_problem(problems, learned, tracker=tracker)
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
    units_tested = set(selected.get("knowledge_units_tested", [])) if selected else set()
    active_mis_for_attempt = (
        list(tracker.get_active_misconception_ids(units_tested)) if selected else []
    )

    if run_attempt and selected:
        filled_code_prompt = None
        if domain_adapter and hasattr(domain_adapter, "get_code_generation_prompt"):
            filled_code_prompt = domain_adapter.get_code_generation_prompt(
                tracker.get_full_state(), selected, active_mis_for_attempt
            )
        ta_code = get_ta_code_attempt(
            selected,
            learned,
            active_misconceptions=active_mis_for_attempt or None,
            force_fail_problem_ids=None,
            filled_prompt=filled_code_prompt,
            use_llm_code=use_llm if filled_code_prompt else False,
        )
        if ta_code:
            record_ta_attempt(
                domain=domain,
                task_id=selected.get("problem_id", ""),
                attempt_id=attempt_id,
                learned_unit_ids=sorted(learned),
                output_summary=(ta_code[:200] + "..." if len(ta_code) > 200 else ta_code),
                guard_passed=True,
                fallback_used=not (use_llm and filled_code_prompt),
                active_misconception_ids=active_mis_for_attempt,
            )
        if ta_code and domain_adapter is not None:
            result = domain_adapter.evaluate_attempt(selected, ta_code)
        elif ta_code:
            result = _evaluate_attempt_python(selected, ta_code)
        else:
            result = None
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
                period=(
                    "during_misconception" if active_mis_for_attempt else "before_misconception"
                ),
            )
            record_evaluation_result(
                domain=domain,
                task_id=selected.get("problem_id", ""),
                attempt_id=attempt_id,
                pass_fail=result.get("passed", False),
                unit_ids_tested=selected.get("knowledge_units_tested", []),
                mastery_level_before=None,
                mastery_level_after=summary.get("overall_level") if summary else None,
                misconception_active_during_attempt=(
                    active_mis_for_attempt[0] if active_mis_for_attempt else None
                ),
            )
            for uid in selected.get("knowledge_units_tested", []):
                record_mastery_update(
                    domain=domain,
                    unit_id=uid,
                    mastery_level=(
                        summary.get("level_per_unit", {}).get(uid, "not_assessed")
                        if summary
                        else "not_assessed"
                    ),
                    pass_rate=summary.get("per_unit_pass_rate", {}).get(uid) if summary else None,
                    attempt_count=1,
                    trigger=attempt_id,
                )

    report = (
        build_mastery_report(selected, learned, result, summary, ta_code)
        if selected
        else build_mastery_report(None, learned, None, None)
    )

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
    """Apply correction (unlearning) for a unit."""
    from src.core.misconception_engine import apply_correction

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
    """Add relearning evidence from a follow-up teaching event."""
    from src.core.misconception_engine import add_relearning_evidence_from_teaching

    domain = tracker.get_domain()
    record_teaching_event(
        domain=domain,
        topic_taught=teaching_event.get("topic_taught", ""),
        knowledge_units_taught=teaching_event.get("knowledge_units_taught", []),
        note=teaching_event.get("note", ""),
        teaching_event_id=teaching_event.get("teaching_event_id"),
    )
    unit_id = (teaching_event.get("knowledge_units_taught", [None]) or [None])[0]
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
    domain_adapter: Any = None,
    problem_id: str | None = None,
) -> dict[str, Any]:
    """Run only task selection -> attempt -> evaluation (no teaching)."""
    domain = tracker.get_domain()
    use_llm = use_llm_code if use_llm_code is not None else _use_llm_code()
    learned = tracker.get_learned_units()
    eligible_ids = get_eligible_problem_ids(problems, learned)
    ineligible = get_ineligible_reasons(problems, learned)
    selected = None
    if problem_id:
        for p in problems:
            if p.get("problem_id") == problem_id and set(p.get("knowledge_units_tested", [])) <= learned:
                selected = p
                break
    if not selected:
        selected = select_problem(problems, learned, tracker=tracker)
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
        filled_code_prompt = None
        if domain_adapter and hasattr(domain_adapter, "get_code_generation_prompt"):
            filled_code_prompt = domain_adapter.get_code_generation_prompt(
                tracker.get_full_state(), selected, []
            )
        ta_code = get_ta_code_attempt(
            selected,
            learned,
            active_misconceptions=None,
            force_fail_problem_ids=None,
            filled_prompt=filled_code_prompt,
            use_llm_code=use_llm if filled_code_prompt else False,
        )
        if ta_code:
            record_ta_attempt(
                domain=domain,
                task_id=selected.get("problem_id", ""),
                attempt_id=attempt_id,
                learned_unit_ids=sorted(learned),
                output_summary=(ta_code[:200] + "..." if len(ta_code) > 200 else ta_code),
                guard_passed=True,
                fallback_used=not (use_llm and filled_code_prompt),
                active_misconception_ids=[],
            )
        if ta_code and domain_adapter is not None:
            result = domain_adapter.evaluate_attempt(selected, ta_code)
        elif ta_code:
            result = _evaluate_attempt_python(selected, ta_code)
        else:
            result = None
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
                    mastery_level=(
                        summary.get("level_per_unit", {}).get(uid, "not_assessed")
                        if summary
                        else "not_assessed"
                    ),
                    pass_rate=summary.get("per_unit_pass_rate", {}).get(uid) if summary else None,
                    attempt_count=2,
                    trigger=attempt_id,
                )

    report = (
        build_mastery_report(selected, learned, result, summary, ta_code)
        if selected
        else build_mastery_report(None, learned, None, None)
    )

    return {
        "selected_problem": selected,
        "ta_code": ta_code,
        "attempt_result": result,
        "mastery_summary": summary,
        "mastery_report": report,
        "pass_fail": result.get("passed") if result else None,
        "learned_units": sorted(learned),
    }
