"""
API integration tests: schemas and route dependencies (without full server).
"""
import pytest
from src.api.schemas import (
    TestRequest,
    TestResponse,
    ComprehensiveTestResponse,
    ComprehensiveTestResultItem,
    TeachRequest,
    TeachResponse,
)


def test_test_request_optional_problem_id():
    r = TestRequest(problem_id=None)
    assert r.problem_id is None
    r2 = TestRequest(problem_id="prob_001")
    assert r2.problem_id == "prob_001"


def test_comprehensive_test_response():
    r = ComprehensiveTestResponse(
        total_run=5,
        total_passed=3,
        results=[
            ComprehensiveTestResultItem(problem_id="p1", passed=True, problem_statement="Say 1"),
            ComprehensiveTestResultItem(problem_id="p2", passed=False, problem_statement="Say 2"),
        ],
        overall_summary="Passed 3/5 problems.",
    )
    assert r.total_run == 5
    assert r.total_passed == 3
    assert len(r.results) == 2
    assert r.results[0].passed is True


def test_teach_request():
    r = TeachRequest(student_input="Variables store values.")
    assert r.student_input == "Variables store values."
