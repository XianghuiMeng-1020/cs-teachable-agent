"""Testing: GET problems, POST test."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas import (
    TestRequest,
    TestResponse,
    ComprehensiveTestResponse,
    ComprehensiveTestResultItem,
)
from src.api.deps import DbSession, CurrentUser
from src.api.session_helpers import get_or_create_teaching_session
from src.db.models import TAInstance, TestAttempt
from src.core.knowledge_state import StateTracker
from src.core.task_engine import (
    load_problems,
    select_problem,
    get_eligible_problem_ids,
)
from src.core.attempt_engine import get_ta_code_attempt
from src.core.evaluator import evaluate_attempt, mastery_summary, build_mastery_report, record_attempt_to_state
from src.core.trace import (
    set_trace_db_session,
    record_task_selection,
    record_ta_attempt,
    record_evaluation_result,
    record_mastery_update,
)
from src.core.misconception_engine import activate_misconception_for_unit
from src.domains.python_domain import PythonDomainAdapter

router = APIRouter(tags=["testing"])

_SEED_DIR = Path(__file__).resolve().parent.parent.parent.parent / "seed"


def _get_ta(ta_id: int, user_id: int, db: DbSession) -> TAInstance:
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == user_id,
    ).first()
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    return ta


def _tracker_from_ta(ta: TAInstance) -> StateTracker:
    adapter = PythonDomainAdapter(seed_dir=_SEED_DIR)
    units = adapter.load_knowledge_units()
    tracker = StateTracker(unit_definitions=units, domain=ta.domain_id)
    if ta.knowledge_state and "units" in ta.knowledge_state:
        for uid, rec in ta.knowledge_state["units"].items():
            if uid in tracker._state:
                tracker._state[uid] = dict(rec)
    return tracker


def _save_tracker_to_ta(ta: TAInstance, tracker: StateTracker, db: DbSession):
    ta.knowledge_state = tracker.get_full_state()
    db.add(ta)
    db.commit()


@router.get("/api/ta/{ta_id}/problems")
def list_problems(ta_id: int, current_user: CurrentUser, db: DbSession):
    ta = _get_ta(ta_id, current_user.id, db)
    tracker = _tracker_from_ta(ta)
    adapter = PythonDomainAdapter(seed_dir=_SEED_DIR)
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
    import uuid as _uuid
    ta = _get_ta(ta_id, user_id, db)
    session = get_or_create_teaching_session(db, ta.id)
    set_trace_db_session(db, session.id)
    tracker = _tracker_from_ta(ta)
    adapter = PythonDomainAdapter(seed_dir=_SEED_DIR)
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
        selected = select_problem(problems, learned)

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
    # If problem targets a misconception and TA doesn't have it active yet, activate it so TA exhibits the bug.
    targeted = selected.get("targeted_misconceptions", [])
    if targeted and not active_mis:
        misconceptions_catalog = adapter.load_misconceptions()
        mis_to_units = {m["id"]: m.get("affected_knowledge_units", []) for m in misconceptions_catalog}
        for mis_id in targeted:
            affected = mis_to_units.get(mis_id, [])
            for uid in units_tested:
                if uid in affected:
                    activate_misconception_for_unit(
                        tracker, uid, mis_id, trigger="task_attempt", trigger_reference=selected.get("problem_id")
                    )
                    active_mis = list(tracker.get_active_misconception_ids(units_tested))
                    break
            if active_mis:
                break

    record_task_selection(
        domain=tracker.get_domain(),
        eligible_unit_ids=sorted(learned),
        selected_task_id=selected.get("problem_id"),
        eligible_task_ids=get_eligible_problem_ids(problems, learned),
    )

    active_mis = list(tracker.get_active_misconception_ids(units_tested))
    filled = adapter.get_code_generation_prompt(
        tracker.get_full_state(), selected, active_mis
    )
    ta_code = get_ta_code_attempt(
        selected,
        learned,
        active_misconceptions=active_mis or None,
        force_fail_problem_ids=None,
        filled_prompt=filled,
        use_llm_code=bool(filled),
    )
    attempt_id = str(_uuid.uuid4())
    record_ta_attempt(
        domain=tracker.get_domain(),
        task_id=selected.get("problem_id", ""),
        attempt_id=attempt_id,
        learned_unit_ids=sorted(learned),
        output_summary=(ta_code[:200] + "..." if len(ta_code) > 200 else ta_code),
        guard_passed=True,
        fallback_used=not bool(filled),
        active_misconception_ids=active_mis,
    )

    result = evaluate_attempt(selected, ta_code) if ta_code else None
    summary = mastery_summary(selected, result, []) if result else None
    if result:
        mis_per_unit = {uid: active_mis[0] for uid in selected.get("knowledge_units_tested", [])} if active_mis else {}
        record_attempt_to_state(
            tracker, selected, result, attempt_id,
            misconception_active_per_unit=mis_per_unit or None,
            period="during_misconception" if active_mis else "before_misconception",
        )
        record_evaluation_result(
            domain=tracker.get_domain(),
            task_id=selected.get("problem_id", ""),
            attempt_id=attempt_id,
            pass_fail=result.get("passed", False),
            unit_ids_tested=selected.get("knowledge_units_tested", []),
            mastery_level_after=summary.get("overall_level") if summary else None,
            misconception_active_during_attempt=active_mis[0] if active_mis else None,
        )
        for uid in selected.get("knowledge_units_tested", []):
            record_mastery_update(
                domain=tracker.get_domain(),
                unit_id=uid,
                mastery_level=summary.get("level_per_unit", {}).get(uid, "not_assessed") if summary else "not_assessed",
                pass_rate=summary.get("per_unit_pass_rate", {}).get(uid) if summary else None,
                attempt_count=1,
                trigger=attempt_id,
            )

    report = build_mastery_report(selected, learned, result, summary, ta_code)
    _save_tracker_to_ta(ta, tracker, db)

    session = get_or_create_teaching_session(db, ta.id)
    test_attempt = TestAttempt(
        session_id=session.id,
        problem_id=selected.get("problem_id", ""),
        ta_code=ta_code or None,
        passed=result.get("passed", False) if result else False,
        execution_output=result.get("stdout") if result else None,
        score=(1.0 if result.get("passed") else 0.0) if result else None,
        misconceptions_active=active_mis or None,
    )
    db.add(test_attempt)
    db.commit()

    return TestResponse(
        problem_id=selected.get("problem_id", ""),
        problem_statement=selected.get("problem_statement", ""),
        ta_code=ta_code or "",
        passed=result.get("passed", False) if result else False,
        details=result.get("details", []) if result else [],
        mastery_report=report,
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
    tracker = _tracker_from_ta(ta)
    adapter = PythonDomainAdapter(seed_dir=_SEED_DIR)
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
