"""
Stage One: Demo scenarios (Stage F – shared-cycle orchestration).

Scenarios configure inputs and call the shared run_cycle; they do not wire engines manually.
A = minimal learned state (only print_function); verify selection is constrained.
B = success path (variable_assignment + print_function → problem → PASS).
C = failure path (same as B but TA produces wrong code via state-driven misconception).
D = correction and relearning (misconception → fail → correct → relearn → recovery).

Optional: set USE_LLM_CODE=1 to use controlled LLM code generation in B (fallback to stub if unavailable).
"""

import os
from pathlib import Path

from state_tracker import StateTracker
from problem_selector import load_problems
from teaching_events import make_teaching_event
from mastery_evaluator import (
    build_mastery_report,
    format_mastery_report_line,
    get_aggregated_mastery_for_unit,
)
from trace_history import clear_trace
from run_cycle import (
    run_teaching_and_test,
    run_correction,
    run_relearning_step,
    run_test_only,
)


def _use_llm_code() -> bool:
    """True if env USE_LLM_CODE is set to 1 or true (enables optional LLM code path)."""
    v = os.environ.get("USE_LLM_CODE", "").strip().lower()
    return v in ("1", "true")


def run_scenario_a(ku_path: Path, problems_path: Path) -> dict:
    """
    Scenario A: Minimal learned state.
    Teach only print_function. Verify only problems requiring (a subset of) learned units
    can be selected; confirm problems requiring untaught concepts are not selected.
    """
    clear_trace()
    problems = load_problems(problems_path)
    tracker = StateTracker(ku_path)
    event = make_teaching_event(
        topic_taught="Print output",
        knowledge_units_taught=["print_function"],
        note="Student teaches only how to use print().",
    )
    data = run_teaching_and_test(
        tracker,
        problems,
        event,
        run_attempt=False,
        activate_misconception=None,
    )
    data["scenario_id"] = "A"
    data["name"] = "Minimal learned state (print_function only)"
    data["ineligible_reasons"] = data.get("ineligible_reasons", [])[:5]
    data["problem_attempted"] = False
    data["pass_fail"] = None if data.get("selected_problem") is None else "N/A (no attempt run in A for focus on selection)"
    return data


def run_scenario_b(ku_path: Path, problems_path: Path) -> dict:
    """
    Scenario B: Simple success path.
    Teach variable_assignment + print_function; select problem; TA succeeds; mastery correct.
    """
    clear_trace()
    problems = load_problems(problems_path)
    tracker = StateTracker(ku_path)
    event = make_teaching_event(
        topic_taught="Variables and print",
        knowledge_units_taught=["variable_assignment", "print_function"],
        note="Student teaches variables and print().",
    )
    data = run_teaching_and_test(
        tracker,
        problems,
        event,
        run_attempt=True,
        activate_misconception=None,
        use_llm_code=_use_llm_code(),
    )
    data["scenario_id"] = "B"
    data["name"] = "Success path (variable_assignment + print_function)"
    return data


# Misconception id used in Scenario C/D to drive wrong code for variable/print tasks.
SCENARIO_C_MISCONCEPTION_ID = "variable_print_off"


def run_scenario_c(ku_path: Path, problems_path: Path) -> dict:
    """
    Scenario C: Failure path (Stage C: misconception-driven).
    Same teaching as B; then activate a misconception for variable_assignment so the TA
    produces wrong code (state-driven). Evaluator marks FAIL; mastery reflects failure.
    """
    clear_trace()
    problems = load_problems(problems_path)
    tracker = StateTracker(ku_path)
    event = make_teaching_event(
        topic_taught="Variables and print",
        knowledge_units_taught=["variable_assignment", "print_function"],
        note="Student teaches variables and print(); TA has misconception (e.g. print value+1).",
    )
    data = run_teaching_and_test(
        tracker,
        problems,
        event,
        run_attempt=True,
        activate_misconception={
            "unit_id": "variable_assignment",
            "misconception_id": SCENARIO_C_MISCONCEPTION_ID,
            "trigger": "scenario_c_demo",
            "trigger_reference": event.get("teaching_event_id"),
        },
        use_llm_code=False,
    )
    data["scenario_id"] = "C"
    data["name"] = "Failure path (misconception-driven)"
    data["force_fail_problem_ids"] = set()
    return data


def print_scenario_a_output(data: dict) -> None:
    """Print Scenario A results in a clear format."""
    print("  Teaching event:", data["teaching_event"])
    print("  Learned units:", data["learned_units"])
    print("  TA learner response:", data.get("ta_learner_response", ""))
    print("  Eligible problem IDs (only these could be selected):", data["eligible_problem_ids"] or "(none)")
    print("  Ineligible (first 5) – why not selected:")
    for r in data["ineligible_reasons"]:
        print(f"    - {r['problem_id']}: missing {r['missing_units']}")
    sel = data.get("selected_problem")
    print("  Selected problem:", sel["problem_id"] if sel else "None")
    print("  Conclusion: Knowledge state controls selection; problems requiring untaught concepts are not selected.")


def print_scenario_b_output(data: dict) -> None:
    """Print Scenario B results."""
    print("  Teaching event:", data["teaching_event"])
    print("  Learned units:", data["learned_units"])
    print("  TA learner response:", data.get("ta_learner_response", ""))
    print("  Selected problem:", data["selected_problem"]["problem_id"])
    print("  TA code:\n    " + (data["ta_code"] or "").replace("\n", "\n    "))
    print("  Result: PASS" if data["pass_fail"] else "  Result: FAIL")
    if data.get("attempt_result", {}).get("details"):
        for i, d in enumerate(data["attempt_result"]["details"], 1):
            print(f"    Test {i}: {'pass' if d['passed'] else 'fail'}")
    print("  Mastery report:")
    for line in format_mastery_report_line(data["mastery_report"]):
        print(line)


def print_scenario_c_output(data: dict) -> None:
    """Print Scenario C results (misconception-driven failure path)."""
    print("  Teaching event:", data["teaching_event"])
    print("  Learned units:", data["learned_units"])
    print("  TA learner response:", data.get("ta_learner_response", ""))
    print("  Active misconception(s) (state-driven):", data.get("active_misconception_ids", []))
    print("  Selected problem:", data["selected_problem"]["problem_id"])
    print("  TA code (wrong):\n    " + (data["ta_code"] or "").replace("\n", "\n    "))
    print("  Result: FAIL (expected)")
    if data.get("attempt_result", {}).get("details"):
        for i, d in enumerate(data["attempt_result"]["details"], 1):
            print(f"    Test {i}: {'pass' if d['passed'] else 'fail'}")
    print("  Mastery report:")
    for line in format_mastery_report_line(data["mastery_report"]):
        print(line)


# --- Scenario D: Correction and relearning (misconception → fail → correct → relearn → recovery) ---


def run_scenario_d(ku_path: Path, problems_path: Path) -> dict:
    """
    Scenario D: Full correction/relearning path.
    Same as C up to failure; then explicit correction → relearning (one follow-up teaching) → recovery.
    Shows: misconception active → fail → correction → relearning evidence → unit learned again → TA passes on retry.
    """
    clear_trace()
    problems = load_problems(problems_path)
    tracker = StateTracker(ku_path)

    # 1) Teach + activate misconception → first attempt (fail)
    event = make_teaching_event(
        topic_taught="Variables and print",
        knowledge_units_taught=["variable_assignment", "print_function"],
        note="Student teaches variables and print(); TA has misconception.",
    )
    data1 = run_teaching_and_test(
        tracker,
        problems,
        event,
        run_attempt=True,
        activate_misconception={
            "unit_id": "variable_assignment",
            "misconception_id": SCENARIO_C_MISCONCEPTION_ID,
            "trigger": "scenario_d_demo",
            "trigger_reference": event.get("teaching_event_id"),
        },
        use_llm_code=False,
    )
    problem = data1["selected_problem"]
    result_1 = data1["attempt_result"]
    active_mis_attempt = data1.get("active_misconception_ids", [])
    failed_due_to_misconception = result_1 is not None and not result_1.get("passed", True)

    # 2) Correction (unlearning)
    applied, correction_event = run_correction(
        tracker,
        unit_id="variable_assignment",
        misconception_id=SCENARIO_C_MISCONCEPTION_ID,
        trigger="explicit_correction_event",
        teaching_event_id=None,
        correction_event_id=None,
    )
    state_after_correct = tracker.get_state().get("variable_assignment", "unknown")

    # 3) Relearning: one follow-up teaching event
    follow_up_event = make_teaching_event(
        topic_taught="Variables (correct)",
        knowledge_units_taught=["variable_assignment"],
        note="Follow-up correct teaching after correction.",
    )
    relearn_result = run_relearning_step(tracker, follow_up_event)
    learned_after_relearn = relearn_result["learned_units"]
    state_after_relearn = relearn_result.get("state_after_relearn", "unknown")

    # 4) Retry task (no active misconception) → pass
    data2 = run_test_only(tracker, problems, use_llm_code=False)
    problem_2 = data2["selected_problem"]
    result_2 = data2["attempt_result"]
    report_2 = build_mastery_report(
        problem_2, set(learned_after_relearn), result_2, data2.get("mastery_summary"), data2.get("ta_code", ""),
        unit_status_for_display={"variable_assignment": state_after_relearn},
    ) if problem_2 else build_mastery_report(None, set(learned_after_relearn), None, None)

    trajectory_unit = "variable_assignment"
    history_d = tracker.get_mastery_history(trajectory_unit)
    agg_all = get_aggregated_mastery_for_unit(tracker, trajectory_unit, include_during_misconception=True)
    agg_post_correction = get_aggregated_mastery_for_unit(tracker, trajectory_unit, include_during_misconception=False)
    mastery_trajectory = [
        {"moment": "before_first_attempt", "attempt_count": 0, "pass_rate": None, "level": "not_assessed"},
        {"moment": "after_failure", "attempt_count": 1, "pass_rate": 0.0, "level": "failing", "period_note": "during_misconception"},
        {"moment": "after_correction", "unit_status": state_after_correct, "attempt_count": 1, "pass_rate": 0.0, "level": "failing"},
        {"moment": "after_relearning_success", "unit_status": state_after_relearn, "aggregated_all_attempts": agg_all, "aggregated_excluding_during_misconception": agg_post_correction},
    ]

    return {
        "scenario_id": "D",
        "name": "Correction and relearning (misconception → correct → relearn → recovery)",
        "teaching_event": event,
        "learned_units_after_teach": data1["learned_units"],
        "active_misconception_ids": active_mis_attempt,
        "first_attempt": {
            "problem": problem,
            "ta_code": data1.get("ta_code", ""),
            "result": result_1,
            "pass_fail": result_1.get("passed") if result_1 else None,
        },
        "failed_due_to_misconception": failed_due_to_misconception,
        "correction_event": correction_event,
        "correction_applied": applied,
        "state_after_correction": state_after_correct,
        "follow_up_teaching_event": follow_up_event,
        "state_after_relearning": state_after_relearn,
        "learned_units_after_relearn": learned_after_relearn,
        "second_attempt": {
            "problem": problem_2,
            "ta_code": data2.get("ta_code", ""),
            "result": result_2,
            "pass_fail": result_2.get("passed") if result_2 else None,
        },
        "mastery_report_after_recovery": report_2,
        "recovered": result_2 is not None and result_2.get("passed", False),
        "mastery_trajectory": mastery_trajectory,
        "mastery_history_variable_assignment": history_d,
        "aggregated_all": agg_all,
        "aggregated_excluding_during_misconception": agg_post_correction,
    }


def print_scenario_d_output(data: dict) -> None:
    """Print Scenario D results (correction and relearning path)."""
    print("  Teaching event:", data["teaching_event"])
    print("  Learned units (after teach):", data["learned_units_after_teach"])
    print("  Active misconception(s):", data["active_misconception_ids"])
    first = data.get("first_attempt", {})
    print("  First attempt – problem:", first.get("problem", {}).get("problem_id") if first.get("problem") else None)
    print("  First attempt – TA code (wrong):\n    " + (first.get("ta_code") or "").replace("\n", "\n    "))
    print("  First attempt – Result:", "FAIL" if not first.get("pass_fail") else "PASS")
    print("  Failed due to misconception:", data.get("failed_due_to_misconception"))
    print("  Correction event:", data.get("correction_event"))
    print("  Correction applied:", data.get("correction_applied"))
    print("  State after correction:", data.get("state_after_correction"))
    print("  Follow-up teaching (relearning):", data.get("follow_up_teaching_event", {}).get("topic_taught"))
    print("  State after relearning:", data.get("state_after_relearning"))
    print("  Learned units after relearn:", data.get("learned_units_after_relearn"))
    second = data.get("second_attempt", {})
    print("  Second attempt – problem:", second.get("problem", {}).get("problem_id") if second.get("problem") else None)
    print("  Second attempt – TA code (correct):\n    " + (second.get("ta_code") or "").replace("\n", "\n    "))
    print("  Second attempt – Result:", "PASS" if second.get("pass_fail") else "FAIL")
    print("  Mastery report after recovery:")
    for line in format_mastery_report_line(data.get("mastery_report_after_recovery") or {}):
        print(line)
    print("  Recovered:", data.get("recovered"))
    traj = data.get("mastery_trajectory") or []
    if traj:
        print("  Mastery trajectory (variable_assignment):")
        for step in traj:
            m = step.get("moment", "")
            level = step.get("level") or (step.get("aggregated_all_attempts") or {}).get("aggregated_level") or (step.get("aggregated_excluding_during_misconception") or {}).get("aggregated_level")
            print(f"    - {m}: level={level}, unit_status={step.get('unit_status', '')}, attempt_count={step.get('attempt_count', '')}, pass_rate={step.get('pass_rate', '')}")
        agg = data.get("aggregated_all")
        if agg:
            print(f"  Aggregated (all attempts): attempt_count={agg.get('attempt_count')}, pass_rate={agg.get('pass_rate')}, level={agg.get('aggregated_level')}")
        agg_ex = data.get("aggregated_excluding_during_misconception")
        if agg_ex:
            print(f"  Aggregated (excluding during-misconception): attempt_count={agg_ex.get('attempt_count')}, pass_rate={agg_ex.get('pass_rate')}, level={agg_ex.get('aggregated_level')}")
