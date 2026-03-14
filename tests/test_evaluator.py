"""
Unit tests for Mastery Evaluator (run code, evaluate attempt, mastery summary).
"""
import pytest
from src.core.evaluator import (
    run_python_code,
    evaluate_attempt,
    mastery_summary,
)


def test_run_python_code_simple():
    stdout, stderr, code = run_python_code("print(42)", "", timeout_seconds=2.0)
    assert code == 0
    assert "42" in stdout


def test_run_python_code_with_stdin():
    code_str = "x = input(); print(x)"
    stdout, stderr, code = run_python_code(code_str, "hello\n", timeout_seconds=2.0)
    assert code == 0
    assert "hello" in stdout


def test_evaluate_attempt_pass():
    problem = {
        "problem_id": "p1",
        "test_cases": [
            {"input": "", "expected_output": "42\n"},
        ],
    }
    result = evaluate_attempt(problem, "print(42)")
    assert result["passed"] is True
    assert len(result["details"]) == 1
    assert result["details"][0]["passed"] is True


def test_evaluate_attempt_fail():
    problem = {
        "problem_id": "p1",
        "test_cases": [
            {"input": "", "expected_output": "42\n"},
        ],
    }
    result = evaluate_attempt(problem, "print(0)")
    assert result["passed"] is False
    assert result["details"][0]["passed"] is False


def test_mastery_summary():
    problem = {"knowledge_units_tested": ["var", "print"]}
    attempt_result = {"passed": True}
    summary = mastery_summary(problem, attempt_result, [])
    assert summary["problem_passed"] is True
    assert summary["per_unit_pass_rate"]["var"] == 1.0
    assert summary["overall_level"] == "proficient"
