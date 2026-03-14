"""Teacher dashboard: list students, analytics, transcripts."""

import csv
import io
from collections import defaultdict
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from src.api.schemas import (
    StudentSummary,
    AnalyticsResponse,
    TranscriptSessionSummary,
    TranscriptListResponse,
    TranscriptMessageSchema,
    TranscriptDetailResponse,
    StudentDetailResponse,
    StudentTADetail,
)
from src.api.deps import DbSession, CurrentUser
from src.db.models import User, TAInstance, TeachingSession, TeachingEvent, TestAttempt

router = APIRouter(prefix="/api/teacher", tags=["teacher"])


def _require_teacher(current_user: CurrentUser):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher access only")


@router.get("/students", response_model=list[StudentSummary])
def list_students(current_user: CurrentUser, db: DbSession):
    _require_teacher(current_user)
    users = db.query(User).filter(User.role == "student").all()
    out = []
    for u in users:
        instances = db.query(TAInstance).filter(TAInstance.user_id == u.id).all()
        domain_ids = list({i.domain_id for i in instances})
        out.append(StudentSummary(
            user_id=u.id,
            username=u.username,
            ta_count=len(instances),
            domain_ids=domain_ids,
        ))
    return out


@router.get("/analytics", response_model=AnalyticsResponse)
def analytics(current_user: CurrentUser, db: DbSession):
    _require_teacher(current_user)
    students = db.query(User).filter(User.role == "student").all()
    student_ids = {u.id for u in students}
    instances = db.query(TAInstance).filter(TAInstance.user_id.in_(student_ids)).all()
    user_by_id = {u.id: u for u in students}

    # Avg mastery: from each TA's knowledge_state learned count / total units
    total_learned = 0
    total_units_count = 0
    mis_counts = defaultdict(int)
    for ta in instances:
        state = ta.knowledge_state or {}
        units = state.get("units", {})
        learned = len([u for u in units.values() if (u or {}).get("status") == "learned"])
        total_learned += learned
        total_units_count += len(units) if units else 20
        for u in (units or {}).values():
            for mid in (u or {}).get("active_misconceptions", []) or []:
                mis_counts[mid] += 1

    avg_mastery = total_learned / total_units_count if total_units_count else None

    # Sessions today: count teaching sessions created today
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    sessions_today = (
        db.query(TeachingSession)
        .join(TAInstance)
        .filter(
            TAInstance.user_id.in_(student_ids),
            TeachingSession.created_at >= today_start,
            TeachingSession.created_at < today_end,
        )
        .count()
    )

    # Knowledge coverage: per unit_id, how many students have it learned
    unit_students = defaultdict(set)
    for ta in instances:
        state = ta.knowledge_state or {}
        units = state.get("units", {})
        for uid, rec in (units or {}).items():
            if (rec or {}).get("status") == "learned":
                unit_students[uid].add(ta.user_id)
    knowledge_coverage = [
        {"unit_id": uid, "students_learned": len(sids), "total_students": len(students)}
        for uid, sids in sorted(unit_students.items())
    ]

    # Per (student, unit) status for heatmap: user_id, unit_id, status
    student_unit_status = []
    for ta in instances:
        state = ta.knowledge_state or {}
        units = state.get("units", {}) or {}
        for uid, rec in units.items():
            status = (rec or {}).get("status", "unknown")
            student_unit_status.append({"user_id": ta.user_id, "unit_id": uid, "status": status})

    # Mastery trend: last 7 days from TestAttempt pass rate per day
    session_ids = [s.id for s in db.query(TeachingSession.id).filter(TeachingSession.ta_instance_id.in_([t.id for t in instances])).all()]
    trend = []
    if session_ids:
        attempts = db.query(TestAttempt).filter(TestAttempt.session_id.in_(session_ids)).all()
        by_date = defaultdict(lambda: {"passed": 0, "total": 0})
        for a in attempts:
            if a.created_at:
                d = (a.created_at.date() if hasattr(a.created_at, "date") else a.created_at[:10])
                by_date[str(d)]["total"] += 1
                if a.passed:
                    by_date[str(d)]["passed"] += 1
        for i in range(7):
            dt = datetime.now(timezone.utc).date() - timedelta(days=6 - i)
            key = str(dt)
            t = by_date.get(key, {"passed": 0, "total": 0})
            trend.append({"date": key, "avg_mastery": t["passed"] / t["total"] if t["total"] else 0.0})
    if not trend:
        trend = [{"date": str(datetime.now(timezone.utc).date()), "avg_mastery": 0.0}]

    # Recent activity: last 20 TeachingEvent + TestAttempt across all sessions
    recent = []
    for te in db.query(TeachingEvent).filter(TeachingEvent.session_id.in_(session_ids)).order_by(TeachingEvent.created_at.desc()).limit(15):
        sess = db.query(TeachingSession).filter(TeachingSession.id == te.session_id).first()
        if sess:
            ta = db.query(TAInstance).filter(TAInstance.id == sess.ta_instance_id).first()
            if ta:
                u = user_by_id.get(ta.user_id)
                uname = u.username if u else "?"
                recent.append({
                    "student": uname,
                    "action": f"taught {te.topic_taught or 'concept'}",
                    "result": None,
                    "timestamp": te.created_at.isoformat() if te.created_at else "",
                })
    for ta_attempt in db.query(TestAttempt).filter(TestAttempt.session_id.in_(session_ids)).order_by(TestAttempt.created_at.desc()).limit(10):
        sess = db.query(TeachingSession).filter(TeachingSession.id == ta_attempt.session_id).first()
        if sess:
            ta = db.query(TAInstance).filter(TAInstance.id == sess.ta_instance_id).first()
            if ta:
                u = user_by_id.get(ta.user_id)
                uname = u.username if u else "?"
                recent.append({
                    "student": uname,
                    "action": "tested",
                    "result": f"{ta_attempt.problem_id} → {'PASS' if ta_attempt.passed else 'FAIL'}",
                    "timestamp": ta_attempt.created_at.isoformat() if ta_attempt.created_at else "",
                })
    recent.sort(key=lambda x: x["timestamp"] or "", reverse=True)
    recent = recent[:20]

    return AnalyticsResponse(
        student_count=len(students),
        avg_mastery=round(avg_mastery, 2) if avg_mastery is not None else None,
        active_misconception_counts=dict(mis_counts),
        knowledge_coverage=knowledge_coverage,
        mastery_trend=trend,
        recent_activity=recent,
        student_unit_status=student_unit_status,
        sessions_today=sessions_today,
    )


@router.get("/transcripts", response_model=TranscriptListResponse)
def list_transcripts(
    current_user: CurrentUser,
    db: DbSession,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    student_id: int | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    search: str | None = Query(None),
    ku: str | None = Query(None, description="Comma-separated KU ids to filter sessions"),
):
    _require_teacher(current_user)
    q = db.query(TeachingSession).join(TAInstance).join(User)
    if student_id is not None:
        q = q.filter(User.id == student_id)
    if search and search.strip():
        term = f"%{search.strip()}%"
        q = q.filter(User.username.ilike(term))
    if date_from:
        q = q.filter(TeachingSession.started_at >= date_from)
    if date_to:
        q = q.filter(TeachingSession.started_at <= date_to)
    q = q.order_by(TeachingSession.started_at.desc())
    if ku and ku.strip():
        ku_ids = [k.strip() for k in ku.split(",") if k.strip()]
        if ku_ids:
            sessions_all = q.all()
            session_ids_with_ku = set()
            for ev in db.query(TeachingEvent).filter(TeachingEvent.interpreted_units.isnot(None)).all():
                units = ev.interpreted_units or []
                if any(u in ku_ids for u in units):
                    session_ids_with_ku.add(ev.session_id)
            sessions = [s for s in sessions_all if s.id in session_ids_with_ku]
            total = len(sessions)
            start = (page - 1) * per_page
            page_sessions = sessions[start : start + per_page]
        else:
            total = q.count()
            start = (page - 1) * per_page
            page_sessions = q.offset(start).limit(per_page).all()
    else:
        total = q.count()
        start = (page - 1) * per_page
        page_sessions = q.offset(start).limit(per_page).all()
    if not page_sessions:
        return TranscriptListResponse(items=[], total=total, page=page, per_page=per_page)
    session_ids = [s.id for s in page_sessions]
    ta_ids = [s.ta_instance_id for s in page_sessions]
    tas = {t.id: t for t in db.query(TAInstance).filter(TAInstance.id.in_(ta_ids)).all()}
    user_ids = list({t.user_id for t in tas.values()})
    users = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()}
    from sqlalchemy import func
    te_counts = {row[0]: row[1] for row in db.query(TeachingEvent.session_id, func.count(TeachingEvent.id)).filter(TeachingEvent.session_id.in_(session_ids)).group_by(TeachingEvent.session_id).all()}
    ta_counts = {row[0]: row[1] for row in db.query(TestAttempt.session_id, func.count(TestAttempt.id)).filter(TestAttempt.session_id.in_(session_ids)).group_by(TestAttempt.session_id).all()}
    all_tes = db.query(TeachingEvent).filter(TeachingEvent.session_id.in_(session_ids)).all()
    kus_by_session = defaultdict(set)
    for te in all_tes:
        for u in (te.interpreted_units or []) or []:
            kus_by_session[te.session_id].add(u)
    items = []
    for sess in page_sessions:
        ta = tas.get(sess.ta_instance_id)
        user = users.get(ta.user_id) if ta else None
        te_count = te_counts.get(sess.id, 0)
        ta_count = ta_counts.get(sess.id, 0)
        msg_count = te_count * 2 + ta_count
        items.append(TranscriptSessionSummary(
            session_id=sess.id,
            student={"id": user.id, "username": user.username} if user else {"id": 0, "username": "?"},
            ta_id=sess.ta_instance_id,
            domain_id=ta.domain_id if ta else "?",
            message_count=msg_count,
            kus_covered=sorted(kus_by_session.get(sess.id, set())),
            started_at=sess.started_at.isoformat() if sess.started_at else "",
            ended_at=sess.ended_at.isoformat() if sess.ended_at else None,
        ))
    return TranscriptListResponse(items=items, total=total, page=page, per_page=per_page)


@router.get("/student/{user_id}/detail", response_model=StudentDetailResponse)
def get_student_detail(user_id: int, current_user: CurrentUser, db: DbSession):
    _require_teacher(current_user)
    user = db.query(User).filter(User.id == user_id, User.role == "student").first()
    if not user:
        raise HTTPException(status_code=404, detail="Student not found")
    instances = db.query(TAInstance).filter(TAInstance.user_id == user.id).all()
    ta_details = []
    for ta in instances:
        state = ta.knowledge_state or {}
        units = state.get("units", {})
        learned = len([u for u in (units or {}).values() if (u or {}).get("status") == "learned"])
        total_kus = len(units) if units else 20
        active_mis = []
        for u in (units or {}).values():
            for mid in (u or {}).get("active_misconceptions", []) or []:
                active_mis.append(mid)
        session_ids = [s.id for s in db.query(TeachingSession.id).filter(TeachingSession.ta_instance_id == ta.id)]
        attempts = db.query(TestAttempt).filter(TestAttempt.session_id.in_(session_ids)).all() if session_ids else []
        test_count = len(attempts)
        pass_rate = sum(1 for a in attempts if a.passed) / test_count if test_count else 0.0
        last_attempt = max((a.created_at for a in attempts), default=None)
        last_active = last_attempt.isoformat() if last_attempt else None
        ta_details.append(StudentTADetail(
            id=ta.id,
            domain_id=ta.domain_id,
            learned_count=learned,
            total_kus=total_kus,
            mastery_percent=round(learned / total_kus * 100) if total_kus else 0,
            active_misconceptions=list(set(active_mis)),
            test_count=test_count,
            pass_rate=round(pass_rate, 2),
            last_active=last_active,
            units=state.get("units"),
        ))
    return StudentDetailResponse(
        user={"id": user.id, "username": user.username, "role": user.role, "created_at": user.created_at.isoformat() if user.created_at else None},
        ta_instances=ta_details,
    )


@router.get("/transcripts/export")
def export_transcripts(
    current_user: CurrentUser,
    db: DbSession,
    session_id: int | None = Query(None),
):
    _require_teacher(current_user)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["session_id", "seq", "speaker", "content", "interpreted_units", "quality_score", "timestamp"])
    if session_id:
        sess = db.query(TeachingSession).filter(TeachingSession.id == session_id).first()
        sessions = [sess] if sess else []
    else:
        sessions = db.query(TeachingSession).order_by(TeachingSession.started_at.desc()).all()
    for sess in sessions:
        for te in db.query(TeachingEvent).filter(TeachingEvent.session_id == sess.id).order_by(TeachingEvent.created_at):
            writer.writerow([sess.id, "", "student", (te.student_input or "")[:500], "", "", te.created_at.isoformat() if te.created_at else ""])
            writer.writerow([sess.id, "", "ta", (te.ta_response or "")[:500], str(te.interpreted_units or []), str(te.quality_score), te.created_at.isoformat() if te.created_at else ""])
        for ta_attempt in db.query(TestAttempt).filter(TestAttempt.session_id == sess.id).order_by(TestAttempt.created_at):
            writer.writerow([sess.id, "", "system", f"Test {ta_attempt.problem_id} {'PASS' if ta_attempt.passed else 'FAIL'}", "", "", ta_attempt.created_at.isoformat() if ta_attempt.created_at else ""])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=transcripts.csv"})


@router.get("/transcripts/{session_id}", response_model=TranscriptDetailResponse)
def get_transcript_detail(session_id: int, current_user: CurrentUser, db: DbSession):
    _require_teacher(current_user)
    sess = db.query(TeachingSession).filter(TeachingSession.id == session_id).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    ta = db.query(TAInstance).filter(TAInstance.id == sess.ta_instance_id).first()
    user = db.query(User).filter(User.id == ta.user_id).first() if ta else None
    messages = []
    seq = 0
    events = []
    for te in db.query(TeachingEvent).filter(TeachingEvent.session_id == sess.id).order_by(TeachingEvent.created_at):
        events.append(("teach_student", te.student_input, None, None, te.created_at))
        events.append(("teach_ta", te.ta_response, te.interpreted_units, te.quality_score, te.created_at))
    for ta_attempt in db.query(TestAttempt).filter(TestAttempt.session_id == sess.id).order_by(TestAttempt.created_at):
        events.append(("test", f"Test: {ta_attempt.problem_id} — {'PASS' if ta_attempt.passed else 'FAIL'}", None, None, ta_attempt.created_at))
    events.sort(key=lambda x: x[4] or "")
    for kind, content, units, score, ts in events:
        seq += 1
        if kind == "teach_student":
            messages.append(TranscriptMessageSchema(seq=seq, type="teach", speaker="student", content=content or "", interpreted_units=None, quality_score=None, timestamp=ts.isoformat() if ts else ""))
        elif kind == "teach_ta":
            messages.append(TranscriptMessageSchema(seq=seq, type="teach", speaker="ta", content=content or "", interpreted_units=units, quality_score=score, timestamp=ts.isoformat() if ts else ""))
        else:
            messages.append(TranscriptMessageSchema(seq=seq, type="test", speaker="system", content=content or "", interpreted_units=None, quality_score=None, timestamp=ts.isoformat() if ts else ""))
    return TranscriptDetailResponse(
        session_id=sess.id,
        student={"id": user.id, "username": user.username} if user else {"id": 0, "username": "?"},
        ta={"id": ta.id, "domain_id": ta.domain_id} if ta else {"id": 0, "domain_id": "?"},
        started_at=sess.started_at.isoformat() if sess.started_at else "",
        messages=messages,
    )
