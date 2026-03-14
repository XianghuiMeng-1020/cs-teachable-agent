"""Testing: GET problems, POST test."""

from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas import (
    TestRequest,
    TestResponse,
    ComprehensiveTestResponse,
    ComprehensiveTestResultItem,
)
from src.api.deps import DbSession, CurrentUser
from src.api.session_helpers import get_or_create_teaching_session
from src.api.domain_helpers import get_domain_adapter, get_tracker_for_ta, save_tracker_to_ta
from src.db.models import TAInstance, TestAttempt
from src.core.task_engine import select_problem, get_eligible_problem_ids
from src.core.evaluator import build_mastery_report
from src.core.orchestrator import run_test_only
from src.core.dialogue_engine import get_reflection_prompt_after_test
from src.core.trace import set_trace_db_session
from src.core.misconception_engine import (
    activate_misconception_for_unit,
    try_auto_activate_misconception_after_fail,
)

router = APIRouter(tags=["testing"])


def _get_ta(ta_id: int, user_id: int, db: DbSession) -> TAInstance:
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == user_id,
    ).first()
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    return ta


@router.get("/api/ta/{ta_id}/problems")
def list_problems(ta_id: int, current_user: CurrentUser, db: DbSession):
    ta = _get_ta(ta_id, current_user.id, db)
    tracker = get_tracker_for_ta(ta)
    adapter = get_domain_adapter(ta.domain_id)
    problems = adapter.load_problems()
    learned = tracker.get_learned_units()
    eligible_ids = get_eligible_problem_ids(problems, learned)
    eligible = [p for p in problems if p.get("problem_id") in eligible_ids]
    return {"problems": eligible, "eligible_ids": eligible_ids}


def _run_single_test(
    ta_id: int,
    user_id: int,
    db: DbSession,
    *,
    problem_id: str | None = None,
) -> TestResponse:
    """Run one test (auto-select or use problem_id). Persists state to DB."""
    ta = _get_ta(ta_id, user_id, db)
    session = get_or_create_teaching_session(db, ta.id)
    set_trace_db_session(db, session.id)
    tracker = get_tracker_for_ta(ta)
    adapter = get_domain_adapter(ta.domain_id)
    problems = adapter.load_problems()
    learned = tracker.get_learned_units()

    selected = None
    if problem_id:
        for p in problems:
            if p.get("problem_id") == problem_id:
                required = set(p.get("knowledge_units_tested", []))
                if required <= learned:
                    selected = p
                    break
    if not selected:
        selected = select_problem(problems, learned, tracker=tracker)

    if not selected:
        return TestResponse(
            problem_id="",
            problem_statement="No eligible problem. Teach more concepts first.",
            ta_code="",
            passed=False,
            details=[],
            mastery_report=build_mastery_report(None, learned, None, None),
        )

    units_tested = set(selected.get("knowledge_units_tested", []))
    active_mis = list(tracker.get_active_misconception_ids(units_tested))
    targeted = selected.get("targeted_misconceptions", [])
    if targeted and not active_mis:
        misconceptions_catalog = adapter.load_misconceptions()
        mis_to_units = {m["id"]: m.get("affected_knowledge_units", []) for m in misconceptions_catalog}
        for mis_id in targeted:
            affected = mis_to_units.get(mis_id, [])
            for uid in units_tested:
                if uid in affected:
                    activate_misconception_for_unit(
                        tracker,
                        uid,
                        mis_id,
                        trigger="task_attempt",
                        trigger_reference=selected.get("problem_id"),
                        affected_units_from_catalog=affected,
                    )
                    break
            else:
                continue
            break

    result = run_test_only(
        tracker,
        problems,
        domain_adapter=adapter,
        problem_id=selected.get("problem_id", ""),
    )
    ta_code = result.get("ta_code", "")
    attempt_result = result.get("attempt_result")
    report = result.get("mastery_report", build_mastery_report(None, learned, None, None))
    active_mis_after = list(tracker.get_active_misconception_ids(units_tested))

    if not result.get("pass_fail") and ta_code and ta.domain_id == "python":
        misconceptions_catalog = adapter.load_misconceptions()
        try_auto_activate_misconception_after_fail(
            tracker, selected, ta_code, misconceptions_catalog
        )

    save_tracker_to_ta(ta, tracker, db)

    session = get_or_create_teaching_session(db, ta.id)
    test_attempt = TestAttempt(
        session_id=session.id,
        problem_id=selected.get("problem_id", ""),
        ta_code=ta_code or None,
        passed=attempt_result.get("passed", False) if attempt_result else False,
        execution_output=attempt_result.get("stdout") if attempt_result else None,
        score=(1.0 if (attempt_result and attempt_result.get("passed")) else 0.0) if attempt_result else None,
        misconceptions_active=active_mis_after or None,
    )
    db.add(test_attempt)
    db.commit()

    reflection = get_reflection_prompt_after_test(
        selected.get("problem_statement", ""),
        attempt_result.get("passed", False) if attempt_result else False,
        ta_code,
    )
    return TestResponse(
        problem_id=selected.get("problem_id", ""),
        problem_statement=selected.get("problem_statement", ""),
        ta_code=ta_code or "",
        passed=attempt_result.get("passed", False) if attempt_result else False,
        details=attempt_result.get("details", []) if attempt_result else [],
        mastery_report=report,
        reflection_prompt=reflection,
    )


@router.post("/api/ta/{ta_id}/test", response_model=TestResponse)
def run_test(
    ta_id: int,
    body: TestRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    return _run_single_test(ta_id, current_user.id, db, problem_id=body.problem_id)


_MAX_COMPREHENSIVE = 20


@router.post("/api/ta/{ta_id}/test/comprehensive", response_model=ComprehensiveTestResponse)
def run_comprehensive_test(
    ta_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Run tests for all eligible problems (up to _MAX_COMPREHENSIVE)."""
    ta = _get_ta(ta_id, current_user.id, db)
    tracker = get_tracker_for_ta(ta)
    adapter = get_domain_adapter(ta.domain_id)
    problems = adapter.load_problems()
    learned = tracker.get_learned_units()
    eligible_ids = get_eligible_problem_ids(problems, learned)
    to_run = eligible_ids[:_MAX_COMPREHENSIVE]
    if not to_run:
        return ComprehensiveTestResponse(
            total_run=0,
            total_passed=0,
            results=[],
            overall_summary="No eligible problems. Teach more concepts first.",
        )
    results: list[ComprehensiveTestResultItem] = []
    for problem_id in to_run:
        resp = _run_single_test(ta_id, current_user.id, db, problem_id=problem_id)
        if resp.problem_id:
            results.append(
                ComprehensiveTestResultItem(
                    problem_id=resp.problem_id,
                    passed=resp.passed,
                    problem_statement=resp.problem_statement,
                )
            )
    total_passed = sum(1 for r in results if r.passed)
    return ComprehensiveTestResponse(
        total_run=len(results),
        total_passed=total_passed,
        results=results,
        overall_summary=f"Passed {total_passed}/{len(results)} problems.",
    )
