"""
Run TA code against problem test cases and compute pass/fail and mastery summary.
Uses subprocess to execute Python with stdin (minimal sandbox).
Supports partial credit, error type classification, and optional AST-based concept check.
"""

import subprocess
import tempfile
from pathlib import Path

# Error type classification
ERROR_SYNTAX = "SyntaxError"
ERROR_RUNTIME = "RuntimeError"
ERROR_LOGIC = "LogicError"
ERROR_TIMEOUT = "TimeoutError"
ERROR_NONE = "None"

# Partial credit: pass when at least this fraction of test cases pass
PARTIAL_PASS_THRESHOLD = 0.8


def run_python_code(
    code: str, stdin_str: str, timeout_seconds: float = 2.0
) -> tuple[str, str, int]:
    """Execute Python code with given stdin. Returns (stdout, stderr, returncode)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
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


def _classify_error(stderr: str, returncode: int, got: str, expected: str) -> str:
    """Classify failure into SyntaxError, RuntimeError, LogicError, TimeoutError."""
    if "timeout" in (stderr or "").lower() or returncode == -1:
        return ERROR_TIMEOUT
    if "SyntaxError" in (stderr or "") or "IndentationError" in (stderr or ""):
        return ERROR_SYNTAX
    if returncode != 0 and stderr:
        return ERROR_RUNTIME
    if returncode == 0 and (got or "").strip() != (expected or "").strip():
        return ERROR_LOGIC
    return ERROR_NONE


def _code_uses_constructs(code: str) -> list[str]:
    """Lightweight heuristic: which Stage One constructs appear in code (for analytics)."""
    out = []
    if "=" in code and "input()" not in code.split("=")[0]:
        out.append("assignment")
    if "print(" in code:
        out.append("print")
    if "input(" in code:
        out.append("input")
    if "if " in code or " elif " in code or " else:" in code:
        out.append("conditional")
    if "for " in code or "while " in code:
        out.append("loop")
    if "[" in code and "]" in code:
        out.append("list")
    return out


def evaluate_attempt(problem: dict, ta_code: str) -> dict:
    """
    Run TA code against each test case. Returns passed, details, partial_score,
    error_type, and optional used_constructs. Partial credit: passed if
    (passed_count / total) >= PARTIAL_PASS_THRESHOLD.
    """
    test_cases = problem.get("test_cases", [])
    details = []
    passed_count = 0
    last_stdout, last_stderr = "", ""
    error_type = ERROR_NONE

    for tc in test_cases:
        stdin_input = tc.get("input", "")
        expected = tc.get("expected_output", "")
        stdout, stderr, returncode = run_python_code(ta_code, stdin_input)
        passed = returncode == 0 and (stdout or "").strip() == (expected or "").strip()
        if passed:
            passed_count += 1
        elif error_type == ERROR_NONE:
            error_type = _classify_error(stderr, returncode, stdout, expected)
        details.append({
            "input": repr(stdin_input),
            "expected": repr(expected),
            "got": repr(stdout),
            "passed": passed,
        })
        last_stdout, last_stderr = stdout, stderr

    total = len(test_cases) if test_cases else 1
    partial_score = passed_count / total if total else 0.0
    all_passed = passed_count == total
    passed_threshold = partial_score >= PARTIAL_PASS_THRESHOLD

    return {
        "passed": all_passed,
        "partial_score": partial_score,
        "passed_count": passed_count,
        "total_count": total,
        "passed_partial_threshold": passed_threshold,
        "error_type": error_type,
        "details": details,
        "stdout": last_stdout,
        "stderr": last_stderr,
        "used_constructs": _code_uses_constructs(ta_code),
    }


def mastery_summary(
    problem: dict, attempt_result: dict, attempted_problems: list[dict]
) -> dict:
    """Per rubric: per-unit pass rate; overall level."""
    passed = attempt_result.get("passed", False)
    units_tested = set(problem.get("knowledge_units_tested", []))
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


PASS_RATE_FAILING = 0.5
PASS_RATE_DEVELOPING = 0.8


def _pass_rate_to_level(pass_rate: float) -> str:
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
    """Aggregate mastery from mastery_history entries."""
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
    count_during = count_after = 0
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
    history = (
        tracker.get_mastery_history(unit_id)
        if hasattr(tracker, "get_mastery_history")
        else []
    )
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
    """Write testing_evidence and mastery_history for each affected unit; update BKT if supported."""
    if not problem or not attempt_result:
        return
    passed = attempt_result.get("passed", False)
    problem_id = problem.get("problem_id", "")
    units_tested = problem.get("knowledge_units_tested", [])
    mis_per_unit = misconception_active_per_unit or {}
    level_this = "proficient" if passed else "failing"
    if hasattr(tracker, "update_bkt_after_observation"):
        tracker.update_bkt_after_observation(units_tested, passed)
    for uid in units_tested:
        if hasattr(tracker, "append_testing_evidence"):
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
    """Build mastery report for display."""
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
        "ta_code_preview": (
            (ta_code[:200] + ("..." if len(ta_code) > 200 else "")) if ta_code else ""
        ),
    }
    if unit_status_for_display:
        out["unit_status"] = unit_status_for_display
    return out
