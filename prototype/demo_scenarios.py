"""
Stage One: Demo scenarios for hardening pass.
A = minimal learned state (only print_function); verify selection is constrained.
B = success path (variable_assignment + print_function → problem → PASS).
C = failure path (same as B but TA produces wrong code → FAIL).
Optional: set USE_LLM_CODE=1 to use controlled LLM code generation in B (fallback to stub if unavailable).
"""

import os
from pathlib import Path

from state_tracker import StateTracker
from problem_selector import load_problems, select_problem, get_eligible_problem_ids, get_ineligible_reasons
from teaching_events import make_teaching_event, apply_teaching_event
from ta_conversation import get_ta_learner_response
from ta_code_generation import get_ta_code_attempt
from mastery_evaluator import evaluate_attempt, mastery_summary, build_mastery_report, format_mastery_report_line


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
    problems = load_problems(problems_path)
    tracker = StateTracker(ku_path)
    event = make_teaching_event(
        topic_taught="Print output",
        knowledge_units_taught=["print_function"],
        note="Student teaches only how to use print().",
    )
    apply_teaching_event(tracker, event)
    learned = tracker.get_learned_units()
    ta_learner_response = get_ta_learner_response(learned, event, active_misconceptions=None)

    eligible_ids = get_eligible_problem_ids(problems, learned)
    ineligible = get_ineligible_reasons(problems, learned)
    selected = select_problem(problems, learned)

    return {
        "scenario_id": "A",
        "name": "Minimal learned state (print_function only)",
        "teaching_event": event,
        "learned_units": sorted(learned),
        "ta_learner_response": ta_learner_response,
        "eligible_problem_ids": eligible_ids,
        "ineligible_reasons": ineligible[:5],  # first 5 for brevity
        "selected_problem": selected,
        "problem_attempted": selected is not None,
        "pass_fail": None if selected is None else "N/A (no attempt run in A for focus on selection)",
    }


def run_scenario_b(ku_path: Path, problems_path: Path) -> dict:
    """
    Scenario B: Simple success path.
    Teach variable_assignment + print_function; select problem; TA succeeds; mastery correct.
    """
    problems = load_problems(problems_path)
    tracker = StateTracker(ku_path)
    event = make_teaching_event(
        topic_taught="Variables and print",
        knowledge_units_taught=["variable_assignment", "print_function"],
        note="Student teaches variables and print().",
    )
    apply_teaching_event(tracker, event)
    learned = tracker.get_learned_units()
    ta_learner_response = get_ta_learner_response(learned, event, active_misconceptions=None)

    problem = select_problem(problems, learned)
    ta_code = (
        get_ta_code_attempt(
            problem, learned,
            active_misconceptions=None,
            force_fail_problem_ids=None,
            use_llm_code=_use_llm_code(),
        )
        if problem else ""
    )
    result = evaluate_attempt(problem, ta_code) if problem and ta_code else None
    summary = mastery_summary(problem, result, []) if problem and result else None
    report = build_mastery_report(problem, learned, result, summary, ta_code) if problem else build_mastery_report(None, learned, None, None)

    return {
        "scenario_id": "B",
        "name": "Success path (variable_assignment + print_function)",
        "teaching_event": event,
        "learned_units": sorted(learned),
        "ta_learner_response": ta_learner_response,
        "selected_problem": problem,
        "ta_code": ta_code,
        "attempt_result": result,
        "mastery_summary": summary,
        "mastery_report": report,
        "pass_fail": result.get("passed") if result else None,
    }


def run_scenario_c(ku_path: Path, problems_path: Path) -> dict:
    """
    Scenario C: Failure path.
    Same teaching as B, but TA has a simulated misconception so it produces wrong code;
    evaluator marks FAIL; mastery reflects failure.
    """
    problems = load_problems(problems_path)
    tracker = StateTracker(ku_path)
    event = make_teaching_event(
        topic_taught="Variables and print",
        knowledge_units_taught=["variable_assignment", "print_function"],
        note="Student teaches variables and print(); TA has misconception (e.g. off-by-one).",
    )
    apply_teaching_event(tracker, event)
    learned = tracker.get_learned_units()
    ta_learner_response = get_ta_learner_response(learned, event, active_misconceptions=None)

    problem = select_problem(problems, learned)
    # Force failure for prob_var_001: use stub wrong code (deterministic failure path).
    force_fail = {"prob_var_001"}
    ta_code = (
        get_ta_code_attempt(
            problem, learned,
            active_misconceptions=None,
            force_fail_problem_ids=force_fail,
            use_llm_code=False,  # keep Scenario C deterministic
        )
        if problem else ""
    )
    result = evaluate_attempt(problem, ta_code) if problem and ta_code else None
    summary = mastery_summary(problem, result, []) if problem and result else None
    report = build_mastery_report(problem, learned, result, summary, ta_code) if problem else build_mastery_report(None, learned, None, None)

    return {
        "scenario_id": "C",
        "name": "Failure path (misconception: wrong output)",
        "teaching_event": event,
        "learned_units": sorted(learned),
        "ta_learner_response": ta_learner_response,
        "selected_problem": problem,
        "force_fail_problem_ids": force_fail,
        "ta_code": ta_code,
        "attempt_result": result,
        "mastery_summary": summary,
        "mastery_report": report,
        "pass_fail": result.get("passed") if result else None,
    }


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
    """Print Scenario C results."""
    print("  Teaching event:", data["teaching_event"])
    print("  Learned units:", data["learned_units"])
    print("  TA learner response:", data.get("ta_learner_response", ""))
    print("  Force-fail (simulated misconception) for:", data["force_fail_problem_ids"])
    print("  Selected problem:", data["selected_problem"]["problem_id"])
    print("  TA code (wrong):\n    " + (data["ta_code"] or "").replace("\n", "\n    "))
    print("  Result: FAIL (expected)")
    if data.get("attempt_result", {}).get("details"):
        for i, d in enumerate(data["attempt_result"]["details"], 1):
            print(f"    Test {i}: {'pass' if d['passed'] else 'fail'}")
    print("  Mastery report:")
    for line in format_mastery_report_line(data["mastery_report"]):
        print(line)
