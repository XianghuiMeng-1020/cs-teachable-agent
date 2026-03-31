"""Assessment API routes: list items, grade, hint, history, recommend."""

from __future__ import annotations

import logging
import os
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from src.api.deps import CurrentUser, CurrentUserOptional, get_db
from src.api.limiter import limiter
from src.core.assessment_engine import build_student_task_response, grade_assessment
from src.core.assessment_hints import generate_assessment_hint
from src.db.models import AdminConfig, AssessmentAttempt, AssessmentItem, StudentFlag, TAInstance

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assessment", tags=["assessment"])


# --------------- Schemas ---------------

class AssessmentItemSummary(BaseModel):
    id: int
    item_id: str
    item_type: str
    title: str
    theme: str | None
    concepts: list[str] | None
    ai_pass_rate: float | None
    difficulty: float | None

    class Config:
        from_attributes = True


class AssessmentItemListResponse(BaseModel):
    items: list[AssessmentItemSummary]
    total: int


class GradeRequest(BaseModel):
    ta_id: int | None = None
    selected_blocks: list[str] | None = None
    selected_answers: dict[str, str] | None = None
    duration_ms: int | None = None
    hints_used: int = 0


class GradeResponse(BaseModel):
    item_type: str
    correct: bool
    feedback: str
    expected_count: int
    selected_count: int
    correct_count: int
    attempt_id: int | None = None


class HintRequest(BaseModel):
    ta_id: int | None = None
    hint_type: Literal["understand", "next-step", "check-one-issue"] = "next-step"
    level: Literal[1, 2, 3] = 1
    selected_blocks: list[str] | None = None
    selected_answers: dict[str, str] | None = None
    last_feedback: dict[str, Any] | None = None
    reflection: str | None = None
    progress_summary: str | None = None
    attempt_number: int | None = None


class HintResponse(BaseModel):
    hint_id: str
    hint_type: str
    level: int
    title: str
    body: str
    target: dict | None
    escalation_available: bool
    model: str


class AttemptHistoryItem(BaseModel):
    id: int
    item_id: str
    item_type: str
    title: str
    is_correct: bool
    score: float | None
    correct_count: int | None
    expected_count: int | None
    hints_used: int
    duration_ms: int | None
    created_at: str | None


class AttemptHistoryResponse(BaseModel):
    attempts: list[AttemptHistoryItem]
    total: int
    stats: dict[str, Any]


# --------------- Endpoints ---------------

@router.get("/items", response_model=AssessmentItemListResponse)
def list_assessment_items(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    item_type: str | None = Query(None, description="Filter by parsons|dropdown|execution-trace"),
    domain_id: str | None = Query(None),
    max_ai_pass_rate: float | None = Query(None, description="Only items with AI pass rate <= this value"),
    concept: str | None = Query(None, description="Filter by concept keyword"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    q = db.query(AssessmentItem)
    if item_type:
        q = q.filter(AssessmentItem.item_type == item_type)
    if domain_id:
        q = q.filter(AssessmentItem.domain_id == domain_id)
    if max_ai_pass_rate is not None:
        q = q.filter(
            (AssessmentItem.ai_pass_rate <= max_ai_pass_rate) | (AssessmentItem.ai_pass_rate.is_(None))
        )
    if concept:
        q = q.filter(AssessmentItem.metadata_concepts.contains(concept))

    total = q.count()
    items = q.order_by(AssessmentItem.ai_pass_rate.asc().nullslast(), AssessmentItem.id).offset(offset).limit(limit).all()

    return AssessmentItemListResponse(
        items=[
            AssessmentItemSummary(
                id=it.id,
                item_id=it.item_id,
                item_type=it.item_type,
                title=it.title,
                theme=it.metadata_theme,
                concepts=it.metadata_concepts,
                ai_pass_rate=it.ai_pass_rate,
                difficulty=it.difficulty,
            )
            for it in items
        ],
        total=total,
    )


@router.get("/items/{item_db_id}")
def get_assessment_item(
    item_db_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    item = db.query(AssessmentItem).filter(AssessmentItem.id == item_db_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assessment item not found")
    return build_student_task_response(item)


@router.post("/items/{item_db_id}/grade", response_model=GradeResponse)
@limiter.limit("30/minute")
def grade_item(
    request: Request,
    item_db_id: int,
    body: GradeRequest,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    item = db.query(AssessmentItem).filter(AssessmentItem.id == item_db_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assessment item not found")

    result = grade_assessment(
        item_type=item.item_type,
        interaction_content=item.interaction_content,
        answer_key=item.answer_key,
        selected_blocks=body.selected_blocks,
        selected_answers=body.selected_answers,
    )

    prev_count = db.query(sa_func.count(AssessmentAttempt.id)).filter(
        AssessmentAttempt.user_id == current_user.id,
        AssessmentAttempt.item_id == item.id,
    ).scalar() or 0

    submission = {}
    if body.selected_blocks is not None:
        submission["selected_blocks"] = body.selected_blocks
    if body.selected_answers is not None:
        submission["selected_answers"] = body.selected_answers

    attempt = AssessmentAttempt(
        user_id=current_user.id,
        ta_instance_id=body.ta_id,
        item_id=item.id,
        attempt_number=prev_count + 1,
        submission=submission,
        is_correct=result["correct"],
        score=result["correct_count"] / max(result["expected_count"], 1),
        expected_count=result["expected_count"],
        selected_count=result["selected_count"],
        correct_count=result["correct_count"],
        duration_ms=body.duration_ms,
        hints_used=body.hints_used,
        feedback=result,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    if body.ta_id and result["correct"]:
        _update_knowledge_state(db, body.ta_id, item)

    return GradeResponse(
        item_type=result["item_type"],
        correct=result["correct"],
        feedback=result["feedback"],
        expected_count=result["expected_count"],
        selected_count=result["selected_count"],
        correct_count=result["correct_count"],
        attempt_id=attempt.id,
    )


@router.post("/items/{item_db_id}/hint", response_model=HintResponse)
@limiter.limit("20/minute")
def get_hint(
    request: Request,
    item_db_id: int,
    body: HintRequest,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    item = db.query(AssessmentItem).filter(AssessmentItem.id == item_db_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assessment item not found")

    task_data = build_student_task_response(item)

    result = generate_assessment_hint(
        task=task_data,
        hint_type=body.hint_type,
        level=body.level,
        selected_blocks=body.selected_blocks,
        selected_answers=body.selected_answers,
        last_feedback=body.last_feedback,
        reflection=body.reflection,
        progress_summary=body.progress_summary,
        attempt_number=body.attempt_number,
    )

    return HintResponse(**result)


@router.get("/history", response_model=AttemptHistoryResponse)
def get_attempt_history(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    ta_id: int | None = Query(None),
    item_type: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    q = (
        db.query(AssessmentAttempt, AssessmentItem)
        .join(AssessmentItem, AssessmentAttempt.item_id == AssessmentItem.id)
        .filter(AssessmentAttempt.user_id == current_user.id)
    )
    if ta_id:
        q = q.filter(AssessmentAttempt.ta_instance_id == ta_id)
    if item_type:
        q = q.filter(AssessmentItem.item_type == item_type)

    total = q.count()
    rows = q.order_by(AssessmentAttempt.created_at.desc()).offset(offset).limit(limit).all()

    attempts_out = []
    for attempt, item in rows:
        attempts_out.append(AttemptHistoryItem(
            id=attempt.id,
            item_id=item.item_id,
            item_type=item.item_type,
            title=item.title,
            is_correct=attempt.is_correct,
            score=attempt.score,
            correct_count=attempt.correct_count,
            expected_count=attempt.expected_count,
            hints_used=attempt.hints_used,
            duration_ms=attempt.duration_ms,
            created_at=str(attempt.created_at) if attempt.created_at else None,
        ))

    total_attempts = db.query(sa_func.count(AssessmentAttempt.id)).filter(
        AssessmentAttempt.user_id == current_user.id
    ).scalar() or 0
    correct_attempts = db.query(sa_func.count(AssessmentAttempt.id)).filter(
        AssessmentAttempt.user_id == current_user.id,
        AssessmentAttempt.is_correct == True,
    ).scalar() or 0
    unique_items_correct = db.query(sa_func.count(sa_func.distinct(AssessmentAttempt.item_id))).filter(
        AssessmentAttempt.user_id == current_user.id,
        AssessmentAttempt.is_correct == True,
    ).scalar() or 0

    return AttemptHistoryResponse(
        attempts=attempts_out,
        total=total,
        stats={
            "total_attempts": total_attempts,
            "correct_attempts": correct_attempts,
            "accuracy": round(correct_attempts / max(total_attempts, 1), 3),
            "unique_items_solved": unique_items_correct,
        },
    )


@router.get("/recommend")
def recommend_items(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    ta_id: int | None = Query(None),
    count: int = Query(5, ge=1, le=20),
):
    """Recommend assessment items based on weakest knowledge areas."""
    solved_item_ids = set(
        row[0] for row in
        db.query(AssessmentAttempt.item_id)
        .filter(AssessmentAttempt.user_id == current_user.id, AssessmentAttempt.is_correct == True)
        .distinct()
        .all()
    )

    q = db.query(AssessmentItem)
    if solved_item_ids:
        q = q.filter(~AssessmentItem.id.in_(solved_item_ids))
    q = q.order_by(AssessmentItem.ai_pass_rate.asc().nullslast(), AssessmentItem.id)

    items = q.limit(count).all()
    return {
        "recommended": [build_student_task_response(it) for it in items],
        "solved_count": len(solved_item_ids),
    }


@router.get("/stats")
def get_assessment_stats(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Get aggregated assessment statistics for the current user."""
    total_items = db.query(sa_func.count(AssessmentItem.id)).scalar() or 0
    total_attempts = db.query(sa_func.count(AssessmentAttempt.id)).filter(
        AssessmentAttempt.user_id == current_user.id
    ).scalar() or 0
    correct_attempts = db.query(sa_func.count(AssessmentAttempt.id)).filter(
        AssessmentAttempt.user_id == current_user.id,
        AssessmentAttempt.is_correct == True,
    ).scalar() or 0
    unique_solved = db.query(sa_func.count(sa_func.distinct(AssessmentAttempt.item_id))).filter(
        AssessmentAttempt.user_id == current_user.id,
        AssessmentAttempt.is_correct == True,
    ).scalar() or 0

    by_type = (
        db.query(AssessmentItem.item_type, sa_func.count(AssessmentAttempt.id))
        .join(AssessmentAttempt, AssessmentAttempt.item_id == AssessmentItem.id)
        .filter(AssessmentAttempt.user_id == current_user.id)
        .group_by(AssessmentItem.item_type)
        .all()
    )

    return {
        "total_items_available": total_items,
        "total_attempts": total_attempts,
        "correct_attempts": correct_attempts,
        "accuracy": round(correct_attempts / max(total_attempts, 1), 3),
        "unique_items_solved": unique_solved,
        "progress_percent": round(unique_solved / max(total_items, 1) * 100, 1),
        "by_type": {t: c for t, c in by_type},
    }


@router.get("/teacher/overview")
def teacher_assessment_overview(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Teacher: get overview of all assessment items and student performance."""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher role required")

    total_items = db.query(sa_func.count(AssessmentItem.id)).scalar() or 0
    total_attempts = db.query(sa_func.count(AssessmentAttempt.id)).scalar() or 0
    total_correct = db.query(sa_func.count(AssessmentAttempt.id)).filter(
        AssessmentAttempt.is_correct == True
    ).scalar() or 0
    unique_students = db.query(sa_func.count(sa_func.distinct(AssessmentAttempt.user_id))).scalar() or 0

    items_by_type = (
        db.query(AssessmentItem.item_type, sa_func.count(AssessmentItem.id))
        .group_by(AssessmentItem.item_type)
        .all()
    )

    from sqlalchemy import case, literal_column
    correct_case = case((AssessmentAttempt.is_correct == True, 1), else_=0)
    hardest_items = (
        db.query(
            AssessmentItem.item_id,
            AssessmentItem.title,
            AssessmentItem.item_type,
            sa_func.count(AssessmentAttempt.id).label("attempts"),
            sa_func.sum(correct_case).label("correct"),
        )
        .join(AssessmentAttempt, AssessmentAttempt.item_id == AssessmentItem.id)
        .group_by(AssessmentItem.id)
        .order_by(
            (sa_func.sum(correct_case) * 1.0 / sa_func.count(AssessmentAttempt.id)).asc()
        )
        .limit(10)
        .all()
    )

    return {
        "total_items": total_items,
        "total_attempts": total_attempts,
        "total_correct": total_correct,
        "overall_accuracy": round(total_correct / max(total_attempts, 1), 3),
        "unique_students": unique_students,
        "items_by_type": {t: c for t, c in items_by_type},
        "hardest_items": [
            {
                "item_id": h.item_id, "title": h.title, "item_type": h.item_type,
                "attempts": h.attempts, "correct": h.correct or 0,
                "pass_rate": round((h.correct or 0) / max(h.attempts, 1), 3),
            }
            for h in hardest_items
        ],
    }


# --------------- Telemetry ---------------

class TelemetryEventBody(BaseModel):
    eventType: str
    sessionId: str
    attemptId: str | None = None
    itemId: int | None = None
    itemType: str | None = None
    payload: dict | None = None
    eventTime: str | None = None


def _telemetry_dir() -> str:
    import os
    d = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
    os.makedirs(d, exist_ok=True)
    return d


class TelemetryEventBodyAuth(TelemetryEventBody):
    """Same as TelemetryEventBody; the endpoint also accepts auth optionally."""
    userId: int | None = None


def _get_admin_config_val(db: Session, key: str, default: Any) -> Any:
    row = db.query(AdminConfig).filter(AdminConfig.key == key).first()
    return row.value if row else default


def _auto_flag(db: Session, body: TelemetryEventBody, user_id: int | None) -> None:
    """Check telemetry event against thresholds and auto-create flags."""
    if not user_id:
        return
    try:
        etype = body.eventType
        session_id = body.sessionId

        if etype == "focus_lost":
            threshold = _get_admin_config_val(db, "focus_loss_threshold", 5)
            import json as _json
            filepath = os.path.join(_telemetry_dir(), "telemetry_events.jsonl")
            session_focus_count = 0
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            ev = _json.loads(line)
                        except Exception:
                            continue
                        if ev.get("sessionId") == session_id and ev.get("eventType") == "focus_lost":
                            session_focus_count += 1
            if session_focus_count >= threshold:
                existing = db.query(StudentFlag).filter(
                    StudentFlag.user_id == user_id,
                    StudentFlag.session_id == session_id,
                    StudentFlag.flag_type == "focus_loss_excess",
                    StudentFlag.resolved == False,
                ).first()
                if not existing:
                    db.add(StudentFlag(
                        user_id=user_id, flag_type="focus_loss_excess",
                        severity="warning",
                        detail={"session_focus_count": session_focus_count, "threshold": threshold},
                        session_id=session_id, item_id=body.itemId,
                    ))
                    db.commit()

        elif etype == "graded_correct":
            min_solve = _get_admin_config_val(db, "min_solve_time_ms", 15000)
            dur = (body.payload or {}).get("durationMs")
            if dur is not None and dur < min_solve:
                db.add(StudentFlag(
                    user_id=user_id, flag_type="rapid_solve",
                    severity="critical",
                    detail={"durationMs": dur, "threshold": min_solve},
                    session_id=session_id, item_id=body.itemId,
                ))
                db.commit()

        elif etype == "paste_blocked":
            db.add(StudentFlag(
                user_id=user_id, flag_type="paste_attempt",
                severity="info",
                detail=body.payload,
                session_id=session_id, item_id=body.itemId,
            ))
            db.commit()

        elif etype == "typing_anomaly":
            typing_enabled = _get_admin_config_val(db, "typing_anomaly_enabled", True)
            if typing_enabled:
                db.add(StudentFlag(
                    user_id=user_id, flag_type="typing_anomaly",
                    severity="warning",
                    detail=body.payload,
                    session_id=session_id, item_id=body.itemId,
                ))
                db.commit()

        elif etype == "devtools_opened":
            db.add(StudentFlag(
                user_id=user_id, flag_type="devtools_opened",
                severity="critical",
                detail=body.payload,
                session_id=session_id, item_id=body.itemId,
            ))
            db.commit()

    except Exception:
        logger.exception("Auto-flag detection error")


@router.post("/telemetry")
async def receive_telemetry(
    body: TelemetryEventBody,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Any = Depends(CurrentUserOptional),
):
    """Receive and persist a telemetry event from the frontend, then auto-flag anomalies."""
    import json, datetime

    user_id = current_user.id if current_user else None

    event = {
        "eventType": body.eventType,
        "sessionId": body.sessionId,
        "attemptId": body.attemptId,
        "itemId": body.itemId,
        "itemType": body.itemType,
        "payload": body.payload,
        "eventTime": body.eventTime or datetime.datetime.utcnow().isoformat(),
        "receivedAt": datetime.datetime.utcnow().isoformat(),
        "userId": user_id,
    }

    filepath = os.path.join(_telemetry_dir(), "telemetry_events.jsonl")
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        logger.exception("Failed to write telemetry event")

    _auto_flag(db, body, user_id)

    return {"ok": True}


@router.get("/metrics")
async def get_metrics_dashboard(
    db: Session = Depends(get_db),
):
    """Return comprehensive metrics for the analytics dashboard."""
    import json, os, datetime
    from collections import Counter, defaultdict

    items = db.query(AssessmentItem).all()
    attempts = db.query(AssessmentAttempt).all()

    type_counts: dict[str, int] = Counter()
    type_ai_rates: dict[str, list[float]] = defaultdict(list)
    theme_data: dict[str, dict] = defaultdict(lambda: {"total": 0, "low_ai": 0, "rates": []})
    ai_buckets: dict[str, dict[str, int]] = {
        "0-25": {"parsons": 0, "dropdown": 0, "execution_trace": 0},
        "26-50": {"parsons": 0, "dropdown": 0, "execution_trace": 0},
        "51-75": {"parsons": 0, "dropdown": 0, "execution_trace": 0},
        "76-100": {"parsons": 0, "dropdown": 0, "execution_trace": 0},
    }

    for item in items:
        itype = item.item_type or "unknown"
        type_counts[itype] += 1
        rate = item.ai_pass_rate
        if rate is not None:
            type_ai_rates[itype].append(rate)
            bucket_key = "0-25" if rate <= 25 else "26-50" if rate <= 50 else "51-75" if rate <= 75 else "76-100"
            if itype in ai_buckets[bucket_key]:
                ai_buckets[bucket_key][itype] += 1
        theme = item.theme or "Other"
        theme_data[theme]["total"] += 1
        if rate is not None:
            theme_data[theme]["rates"].append(rate)
            if rate <= 50:
                theme_data[theme]["low_ai"] += 1

    type_overview = []
    for itype, count in type_counts.items():
        rates = type_ai_rates.get(itype, [])
        type_overview.append({
            "item_type": itype,
            "total_items": count,
            "evaluated_items": len(rates),
            "low_ai_items": sum(1 for r in rates if r <= 50),
            "avg_ai_pass_rate": round(sum(rates) / len(rates), 1) if rates else None,
        })

    theme_overview = []
    for theme, d in sorted(theme_data.items(), key=lambda x: x[1]["total"], reverse=True):
        theme_overview.append({
            "theme": theme,
            "total_items": d["total"],
            "low_ai_items": d["low_ai"],
            "avg_ai_pass_rate": round(sum(d["rates"]) / len(d["rates"]), 1) if d["rates"] else None,
        })

    ai_pass_distribution = []
    for bucket_label, by_type in ai_buckets.items():
        ai_pass_distribution.append({
            "bucket": bucket_label,
            "parsons": by_type.get("parsons", 0),
            "dropdown": by_type.get("dropdown", 0),
            "execution_trace": by_type.get("execution_trace", 0),
        })

    # Telemetry from JSONL
    telemetry_events: list[dict] = []
    telem_path = os.path.join(_telemetry_dir(), "telemetry_events.jsonl")
    if os.path.exists(telem_path):
        try:
            with open(telem_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        telemetry_events.append(json.loads(line))
        except Exception:
            pass

    event_type_counts = Counter(e.get("eventType", "?") for e in telemetry_events)
    focus_loss_count = event_type_counts.get("focus_lost", 0)
    resume_count = event_type_counts.get("resume_clicked", 0)

    event_breakdown = [
        {"event_type": k, "count": v}
        for k, v in sorted(event_type_counts.items(), key=lambda x: x[1], reverse=True)
    ]

    total_attempts_db = len(attempts)
    correct_attempts = sum(1 for a in attempts if a.is_correct)

    all_ai_rates = [item.ai_pass_rate for item in items if item.ai_pass_rate is not None]

    return {
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "totals": {
            "total_items": len(items),
            "evaluated_items": sum(len(v) for v in type_ai_rates.values()),
            "low_ai_items": sum(1 for r in all_ai_rates if r <= 50),
            "avg_ai_pass_rate": round(sum(all_ai_rates) / len(all_ai_rates), 1) if all_ai_rates else None,
            "total_attempts": total_attempts_db,
            "correct_attempts": correct_attempts,
            "telemetry_events": len(telemetry_events),
        },
        "type_overview": type_overview,
        "ai_pass_distribution": ai_pass_distribution,
        "theme_overview": theme_overview,
        "telemetry": {
            "available": len(telemetry_events) > 0,
            "total_events": len(telemetry_events),
            "focus_loss_count": focus_loss_count,
            "resume_count": resume_count,
            "event_breakdown": event_breakdown,
        },
    }


def _update_knowledge_state(db: Session, ta_id: int, item: AssessmentItem) -> None:
    """Update TA knowledge state after a correct assessment attempt."""
    try:
        from src.core.knowledge_state import StateTracker
        from src.domains.python.adapter import PythonDomainAdapter

        ta = db.query(TAInstance).filter(TAInstance.id == ta_id).first()
        if not ta:
            return

        adapter = PythonDomainAdapter()
        tracker = StateTracker(unit_definitions=adapter.get_knowledge_units())
        if ta.knowledge_state and "units" in ta.knowledge_state:
            tracker.merge_persisted_state(
                ta.knowledge_state["units"],
                ta.knowledge_state.get("reflection_store"),
            )

        concepts = item.metadata_concepts or []
        tracker.update_from_assessment(concepts, correct=True)

        ta.knowledge_state = tracker.get_full_state()
        db.commit()
    except Exception:
        logger.exception("Failed to update knowledge state after assessment")
