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


def build_mastery_report(
    problem: dict | None,
    learned_unit_ids: set[str],
    attempt_result: dict | None,
    summary: dict | None,
    ta_code: str = "",
) -> dict:
    """
    Build an informative mastery report for a scenario.
    - selected_problem_id, required_kus, learned_kus_at_attempt, pass_fail,
    - per_problem_interpretation, overall_summary.
    """
    if problem is None:
        return {
            "selected_problem_id": None,
            "required_kus": [],
            "learned_kus_at_attempt": sorted(learned_unit_ids),
            "pass_fail": None,
            "per_problem_interpretation": "No problem attempted.",
            "overall_summary": "No problem selected or attempted.",
        }
    required = sorted(problem.get("knowledge_units_tested", []))
    passed = attempt_result.get("passed", False) if attempt_result else False
    level_per_unit = summary.get("level_per_unit", {}) if summary else {}
    overall_level = summary.get("overall_level", "not_assessed") if summary else "not_assessed"
    return {
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
    if report.get("ta_code_preview"):
        lines.append(f"  TA code (preview): {report['ta_code_preview']}")
    return lines
