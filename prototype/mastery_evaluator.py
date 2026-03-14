"""
Stage One: Run TA code against problem test cases and compute pass/fail and mastery summary.
Uses subprocess to execute Python with stdin; no sandbox (minimal local prototype).
"""

import subprocess
import tempfile
from pathlib import Path


def run_python_code(code: str, stdin_str: str, timeout_seconds: float = 2.0) -> tuple[str, str, int]:
    """
    Execute Python code with given stdin. Returns (stdout, stderr, returncode).
    Writes code to a temp file and runs it. Not a secure sandbox.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = Path(f.name)
    try:
        result = subprocess.run(
            ["python", str(path)],
            input=stdin_str,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=path.parent,
        )
        return (result.stdout or "", result.stderr or "", result.returncode)
    except subprocess.TimeoutExpired:
        return ("", "timeout", -1)
    finally:
        path.unlink(missing_ok=True)


def evaluate_attempt(problem: dict, ta_code: str) -> dict:
    """
    Run TA code against each test case. Problem passes iff all test cases pass.
    Returns dict: passed (bool), details (list of per-test-case results), stdout/stderr from last run.
    """
    test_cases = problem.get("test_cases", [])
    details = []
    all_passed = True
    last_stdout, last_stderr = "", ""

    for tc in test_cases:
        stdin_input = tc.get("input", "")
        expected = tc.get("expected_output", "")
        stdout, stderr, returncode = run_python_code(ta_code, stdin_input)
        passed = returncode == 0 and (stdout or "") == (expected or "")
        details.append({
            "input": repr(stdin_input),
            "expected": repr(expected),
            "got": repr(stdout),
            "passed": passed,
        })
        if not passed:
            all_passed = False
        last_stdout, last_stderr = stdout, stderr

    return {
        "passed": all_passed,
        "details": details,
        "stdout": last_stdout,
        "stderr": last_stderr,
    }


def mastery_summary(problem: dict, attempt_result: dict, attempted_problems: list[dict]) -> dict:
    """
    Per rubric: per-unit pass rate over attempted problems that test that unit;
    overall pass rate. For single-problem demo, one result.
    attempted_problems: list of { problem, passed } for history (this run we only have one).
    """
    passed = attempt_result.get("passed", False)
    units_tested = set(problem.get("knowledge_units_tested", []))
    # Single attempt: each unit gets 1.0 if passed else 0.0; overall same.
    per_unit = {uid: 1.0 if passed else 0.0 for uid in units_tested}
    return {
        "problem_passed": passed,
        "per_unit_pass_rate": per_unit,
        "overall_pass_rate": 1.0 if passed else 0.0,
        "level_per_unit": {
            uid: "proficient" if (1.0 if passed else 0.0) >= 0.8 else "failing"
            for uid in units_tested
        },
        "overall_level": "proficient" if passed else "failing",
    }


# Rubric thresholds (mastery-rubric-stage1.md)
PASS_RATE_FAILING = 0.5
PASS_RATE_DEVELOPING = 0.8


def _pass_rate_to_level(pass_rate: float) -> str:
    """Map pass_rate to mastery level: failing / developing / proficient."""
    if pass_rate >= PASS_RATE_DEVELOPING:
        return "proficient"
    if pass_rate >= PASS_RATE_FAILING:
        return "developing"
    return "failing"


def aggregate_mastery(
    history_entries: list[dict],
    *,
    include_during_misconception: bool = True,
) -> dict:
    """
    Aggregate mastery from a list of mastery_history entries (Stage E).
    Returns attempt_count, pass_count, pass_rate, aggregated_level.
    If include_during_misconception is False, only entries without misconception_active_during_attempt
    (or period != during_misconception) are counted, so "current" mastery can reflect post-correction only.
    """
    if not history_entries:
        return {
            "attempt_count": 0,
            "pass_count": 0,
            "pass_rate": 0.0,
            "aggregated_level": "not_assessed",
            "count_during_misconception": 0,
            "count_after_correction": 0,
        }
    filtered = []
    count_during = 0
    count_after = 0
    for e in history_entries:
        mis = e.get("misconception_active_during_attempt")
        period = e.get("period")
        if period == "during_misconception" or mis:
            count_during += 1
        if period == "after_correction":
            count_after += 1
        if include_during_misconception or not (period == "during_misconception" or mis):
            filtered.append(e)
    if not filtered:
        return {
            "attempt_count": 0,
            "pass_count": 0,
            "pass_rate": 0.0,
            "aggregated_level": "not_assessed",
            "attempt_count_total": len(history_entries),
            "count_during_misconception": count_during,
            "count_after_correction": count_after,
        }
    pass_count = sum(1 for e in filtered if e.get("pass_fail"))
    attempt_count = len(filtered)
    pass_rate = pass_count / attempt_count if attempt_count else 0.0
    return {
        "attempt_count": attempt_count,
        "pass_count": pass_count,
        "pass_rate": pass_rate,
        "aggregated_level": _pass_rate_to_level(pass_rate),
        "attempt_count_total": len(history_entries),
        "count_during_misconception": count_during,
        "count_after_correction": count_after,
    }


def get_aggregated_mastery_for_unit(
    tracker,
    unit_id: str,
    *,
    include_during_misconception: bool = True,
) -> dict:
    """Read unit's mastery_history from state and return aggregated mastery (Stage E)."""
    history = tracker.get_mastery_history(unit_id) if hasattr(tracker, "get_mastery_history") else []
    return aggregate_mastery(history, include_during_misconception=include_during_misconception)


def record_attempt_to_state(
    tracker,
    problem: dict,
    attempt_result: dict,
    attempt_id: str,
    *,
    misconception_active_per_unit: dict[str, str] | None = None,
    period: str | None = None,
) -> None:
    """
    After an evaluated attempt, write testing_evidence and mastery_history entry for each
    affected unit (Stage E). misconception_active_per_unit: unit_id -> misconception_id or None.
    period: one of before_misconception, during_misconception, after_correction.
    """
    if not problem or not attempt_result:
        return
    passed = attempt_result.get("passed", False)
    problem_id = problem.get("problem_id", "")
    units_tested = problem.get("knowledge_units_tested", [])
    mis_per_unit = misconception_active_per_unit or {}
    level_this = "proficient" if passed else "failing"
    for uid in units_tested:
        if not hasattr(tracker, "append_testing_evidence"):
            continue
        tracker.append_testing_evidence(
            uid,
            task_id=problem_id,
            attempt_id=attempt_id,
            pass_fail=passed,
            mastery_level_at_attempt=level_this,
            misconception_active_during_attempt=mis_per_unit.get(uid),
        )
        if hasattr(tracker, "append_mastery_history_entry"):
            tracker.append_mastery_history_entry(
                uid,
                attempt_id=attempt_id,
                problem_id=problem_id,
                pass_fail=passed,
                mastery_level=level_this,
                misconception_active_during_attempt=mis_per_unit.get(uid),
                period=period,
            )


def build_mastery_report(
    problem: dict | None,
    learned_unit_ids: set[str],
    attempt_result: dict | None,
    summary: dict | None,
    ta_code: str = "",
    unit_status_for_display: dict[str, str] | None = None,
) -> dict:
    """
    Build an informative mastery report for a scenario.
    - selected_problem_id, required_kus, learned_kus_at_attempt, pass_fail,
    - per_problem_interpretation, overall_summary.
    - unit_status_for_display: optional map unit_id -> status (e.g. corrected, learned) for Stage D.
    """
    if problem is None:
        out = {
            "selected_problem_id": None,
            "required_kus": [],
            "learned_kus_at_attempt": sorted(learned_unit_ids),
            "pass_fail": None,
            "per_problem_interpretation": "No problem attempted.",
            "overall_summary": "No problem selected or attempted.",
        }
        if unit_status_for_display:
            out["unit_status"] = unit_status_for_display
        return out
    required = sorted(problem.get("knowledge_units_tested", []))
    passed = attempt_result.get("passed", False) if attempt_result else False
    level_per_unit = summary.get("level_per_unit", {}) if summary else {}
    overall_level = summary.get("overall_level", "not_assessed") if summary else "not_assessed"
    out = {
        "selected_problem_id": problem.get("problem_id"),
        "required_kus": required,
        "learned_kus_at_attempt": sorted(learned_unit_ids),
        "pass_fail": "PASS" if passed else "FAIL",
        "per_problem_interpretation": (
            f"Units tested: {required}. Levels: {level_per_unit}. "
            f"All required units were learned; TA attempt {'passed' if passed else 'failed'} test cases."
        ),
        "overall_summary": f"Overall: {overall_level} (one problem, {'passed' if passed else 'failed'}).",
        "ta_code_preview": ta_code[:200] + ("..." if len(ta_code) > 200 else "") if ta_code else "",
    }
    if unit_status_for_display:
        out["unit_status"] = unit_status_for_display
    return out


def format_mastery_report_line(report: dict) -> list[str]:
    """Turn build_mastery_report output into lines for printing."""
    lines = [
        f"  Selected problem: {report.get('selected_problem_id', 'N/A')}",
        f"  Required KUs: {report.get('required_kus', [])}",
        f"  Learned KUs at attempt: {report.get('learned_kus_at_attempt', [])}",
        f"  Pass/Fail: {report.get('pass_fail', 'N/A')}",
        f"  Per-problem: {report.get('per_problem_interpretation', '')}",
        f"  Overall: {report.get('overall_summary', '')}",
    ]
    if report.get("unit_status"):
        lines.append(f"  Unit status (for display): {report['unit_status']}")
    if report.get("ta_code_preview"):
        lines.append(f"  TA code (preview): {report['ta_code_preview']}")
    return lines
