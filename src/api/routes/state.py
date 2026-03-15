"""State: GET state, mastery, trace, misconceptions, history."""

from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.schemas import (
    StateResponse,
    MasteryResponse,
    HistoryResponse,
    HistoryItem,
    MisconceptionsResponse,
    MisconceptionDetail,
)
from src.api.deps import DbSession, CurrentUser
from src.api.domain_helpers import get_domain_adapter, get_tracker_for_ta
from src.core.misconception_engine import get_adaptive_remediation_hint
from src.core.adaptive_learning import recommend_next_kus, estimate_minutes_per_ku
from src.db.models import TAInstance, TeachingSession, TeachingEvent, TestAttempt, TraceEvent

router = APIRouter(tags=["state"])


def _get_ta(ta_id: int, user_id: int, db: DbSession) -> TAInstance:
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == user_id,
    ).first()
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    return ta


@router.get("/api/ta/{ta_id}/state", response_model=StateResponse)
def get_state(ta_id: int, current_user: CurrentUser, db: DbSession):
    ta = _get_ta(ta_id, current_user.id, db)
    tracker = get_tracker_for_ta(ta)
    full = tracker.get_full_state()
    units = full.get("units", {})
    learned = list(tracker.get_learned_units())
    active_mis = tracker.get_active_misconception_ids()
    adapter = get_domain_adapter(ta.domain_id)
    kus = adapter.load_knowledge_units()
    definitions = [
        {"id": u["id"], "name": u.get("name", u["id"]), "prerequisites": u.get("prerequisites", []), "topic_group": u.get("topic_group")}
        for u in kus
    ]
    return StateResponse(
        domain=tracker.get_domain(),
        units=units,
        learned_unit_ids=learned,
        active_misconception_ids=active_mis,
        knowledge_unit_definitions=definitions,
    )


@router.get("/api/ta/{ta_id}/learning-path")
def get_learning_path(ta_id: int, current_user: CurrentUser, db: DbSession):
    """Return recommended next KUs and estimated time to complete."""
    ta = _get_ta(ta_id, current_user.id, db)
    tracker = get_tracker_for_ta(ta)
    adapter = get_domain_adapter(ta.domain_id)
    kus = adapter.load_knowledge_units()
    definitions = [
        {"id": u["id"], "name": u.get("name", u["id"]), "prerequisites": u.get("prerequisites", []), "topic_group": u.get("topic_group")}
        for u in kus
    ]
    learned = set(tracker.get_learned_units())
    recommended = recommend_next_kus(definitions, learned)
    total = len(definitions)
    remaining = total - len(learned)
    minutes_per = estimate_minutes_per_ku()
    return {
        "recommended": recommended[:5],
        "learned_count": len(learned),
        "total_count": total,
        "estimated_minutes_remaining": remaining * minutes_per,
    }


@router.get("/api/ta/{ta_id}/mastery", response_model=MasteryResponse)
def get_mastery(ta_id: int, current_user: CurrentUser, db: DbSession):
    ta = _get_ta(ta_id, current_user.id, db)
    tracker = get_tracker_for_ta(ta)
    learned = list(tracker.get_learned_units())
    session_ids = [s.id for s in db.query(TeachingSession.id).filter(TeachingSession.ta_instance_id == ta.id)]
    attempts = db.query(TestAttempt).filter(TestAttempt.session_id.in_(session_ids)).all() if session_ids else []
    test_count = len(attempts)
    pass_count = sum(1 for a in attempts if a.passed)
    pass_rate = (pass_count / test_count) if test_count else None
    units = tracker.get_full_state().get("units", {})
    total_kus = len(units) or 1
    mastery_percent = round(len(learned) / total_kus * 100) if total_kus else 0
    report = {
        "selected_problem_id": None,
        "required_kus": [],
        "learned_kus_at_attempt": sorted(learned),
        "pass_fail": None,
        "overall_summary": f"Learned units: {len(learned)}. Run a test to see mastery."
        if not test_count
        else f"Learned: {len(learned)}. Tests: {pass_count}/{test_count} passed.",
        "per_problem_interpretation": None,
        "ta_code_preview": None,
        "mastery_percent": mastery_percent,
        "pass_rate": round(pass_rate, 2) if pass_rate is not None else None,
        "test_count": test_count or None,
    }
    return MasteryResponse(**report)


@router.get("/api/ta/{ta_id}/bkt")
def get_bkt(ta_id: int, current_user: CurrentUser, db: DbSession):
    """Return decayed p_know per knowledge unit (BKT state) for analytics."""
    ta = _get_ta(ta_id, current_user.id, db)
    tracker = get_tracker_for_ta(ta)
    return {"p_know": tracker.get_bkt_state()}


@router.get("/api/ta/{ta_id}/trace")
def get_trace(
    ta_id: int,
    current_user: CurrentUser,
    db: DbSession,
    event_type: str | None = Query(None, description="Filter by event_type"),
    date_from: str | None = Query(None, description="ISO date from (inclusive)"),
    date_to: str | None = Query(None, description="ISO date to (inclusive)"),
):
    ta = _get_ta(ta_id, current_user.id, db)
    session_ids = [s.id for s in db.query(TeachingSession.id).filter(TeachingSession.ta_instance_id == ta.id)]
    if not session_ids:
        return {"events": []}
    q = db.query(TraceEvent).filter(TraceEvent.session_id.in_(session_ids))
    if event_type:
        q = q.filter(TraceEvent.event_type == event_type)
    if date_from:
        try:
            from datetime import datetime
            q = q.filter(TraceEvent.created_at >= datetime.fromisoformat(date_from.replace("Z", "+00:00")))
        except ValueError:
            pass
    if date_to:
        try:
            from datetime import datetime
            q = q.filter(TraceEvent.created_at <= datetime.fromisoformat(date_to.replace("Z", "+00:00")))
        except ValueError:
            pass
    rows = q.order_by(TraceEvent.created_at.asc()).all()
    events = []
    for row in rows:
        payload = dict(row.payload or {})
        payload["event_type"] = row.event_type
        payload["timestamp"] = row.created_at.isoformat() if row.created_at else ""
        events.append(payload)
    return {"events": events}


@router.get("/api/ta/{ta_id}/misconceptions", response_model=MisconceptionsResponse)
def get_misconceptions(ta_id: int, current_user: CurrentUser, db: DbSession):
    ta = _get_ta(ta_id, current_user.id, db)
    tracker = get_tracker_for_ta(ta)
    active_ids = tracker.get_active_misconception_ids()
    adapter = get_domain_adapter(ta.domain_id)
    raw_mis = adapter.load_misconceptions()
    by_id = {m["id"]: m for m in raw_mis}
    full_state = tracker.get_full_state()
    units = full_state.get("units", {})
    severity_by_mid: dict[str, tuple[float, int, str]] = {}
    for uid, rec in units.items():
        for am in rec.get("active_misconceptions", []):
            mid = am.get("misconception_id")
            if mid and mid not in severity_by_mid:
                severity_by_mid[mid] = (
                    float(am.get("severity_score", 0)),
                    int(am.get("trigger_count", 1)),
                    am.get("activated_at") or "",
                )
    misconceptions = []
    for mid in active_ids:
        m = by_id.get(mid)
        if m:
            sev, count, activated_at = severity_by_mid.get(mid, (0.0, 1, ""))
            remediation = get_adaptive_remediation_hint(m, severity_score=sev, trigger_count=count)
            misconceptions.append(
                MisconceptionDetail(
                    id=m["id"],
                    description=m.get("description", ""),
                    affected_units=m.get("affected_knowledge_units", []),
                    remediation_hint=remediation,
                    status="active",
                    activated_at=activated_at or None,
                    severity_score=sev if sev else None,
                    trigger_count=count if count else None,
                )
            )
    return MisconceptionsResponse(
        active_misconception_ids=active_ids,
        misconceptions=misconceptions,
    )


@router.get("/api/ta/{ta_id}/history", response_model=HistoryResponse)
def get_history(
    ta_id: int,
    current_user: CurrentUser,
    db: DbSession,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    type_filter: str = Query("all", alias="type"),
):
    ta = _get_ta(ta_id, current_user.id, db)
    session_ids = [s.id for s in db.query(TeachingSession.id).filter(TeachingSession.ta_instance_id == ta.id)]
    if not session_ids:
        return HistoryResponse(items=[], total=0, page=page, per_page=per_page)

    items_raw = []
    for te in db.query(TeachingEvent).filter(TeachingEvent.session_id.in_(session_ids)).order_by(TeachingEvent.created_at.desc()):
        ts = te.created_at.isoformat() if te.created_at else ""
        student_preview = (te.student_input or "")[:80]
        if (te.student_input or "").__len__() > 80:
            student_preview += "..."
        items_raw.append({
            "ts": te.created_at,
            "id": f"te_{te.id}",
            "type": "teach",
            "title": f"Taught {te.topic_taught or 'concept'}",
            "description": f"Student: '{student_preview}'",
            "timestamp": ts,
            "metadata": {"interpreted_units": te.interpreted_units or [], "quality_score": te.quality_score},
        })
    for ta_attempt in db.query(TestAttempt).filter(TestAttempt.session_id.in_(session_ids)).order_by(TestAttempt.created_at.desc()):
        ts = ta_attempt.created_at.isoformat() if ta_attempt.created_at else ""
        ev_type = "test_pass" if ta_attempt.passed else "test_fail"
        items_raw.append({
            "ts": ta_attempt.created_at,
            "id": f"ta_{ta_attempt.id}",
            "type": ev_type,
            "title": f"Tested {ta_attempt.problem_id} → {'PASS' if ta_attempt.passed else 'FAIL'}",
            "description": f"Misconception: {(ta_attempt.misconceptions_active or [None])[0]}" if ta_attempt.misconceptions_active else "Test run.",
            "timestamp": ts,
            "metadata": {"problem_id": ta_attempt.problem_id, "ta_code": ta_attempt.ta_code, "passed": ta_attempt.passed},
        })

    items_raw.sort(key=lambda x: x["ts"] or "", reverse=True)
    if type_filter != "all" and type_filter in ("teach", "test_pass", "test_fail"):
        items_raw = [i for i in items_raw if i["type"] == type_filter]
    total = len(items_raw)
    start = (page - 1) * per_page
    page_items = items_raw[start : start + per_page]

    return HistoryResponse(
        items=[
            HistoryItem(
                id=i["id"],
                type=i["type"],
                title=i["title"],
                description=i["description"],
                timestamp=i["timestamp"],
                metadata=i.get("metadata"),
            )
            for i in page_items
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/api/ta/{ta_id}/messages")
def get_messages(ta_id: int, current_user: CurrentUser, db: DbSession):
    """Return conversation history (student + TA messages) for this TA's sessions."""
    ta = _get_ta(ta_id, current_user.id, db)
    session_ids = [s.id for s in db.query(TeachingSession.id).filter(TeachingSession.ta_instance_id == ta.id)]
    if not session_ids:
        return {"messages": []}
    events = (
        db.query(TeachingEvent)
        .filter(TeachingEvent.session_id.in_(session_ids))
        .order_by(TeachingEvent.created_at.asc())
        .all()
    )
    messages = []
    for te in events:
        if te.student_input:
            messages.append({"role": "student", "content": te.student_input, "timestamp": te.created_at.isoformat() if te.created_at else ""})
        if te.ta_response:
            messages.append({"role": "ta", "content": te.ta_response, "timestamp": te.created_at.isoformat() if te.created_at else ""})
    return {"messages": messages}
