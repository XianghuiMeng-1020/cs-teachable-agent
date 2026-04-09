"""
Learning Analytics Report Generation

Generates comprehensive learning reports for students and teachers.
Supports PDF-ready HTML and JSON data export.
"""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import func, and_

from src.api.deps import DbSession, CurrentUser
from src.api.domain_helpers import get_tracker_for_ta
from src.db.models import (
    TAInstance, TeachingSession, TeachingEvent, 
    TestAttempt, GamificationProfile, User
)

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _get_learning_analytics(ta_id: int, user_id: int, db: DbSession) -> dict:
    """Generate comprehensive learning analytics for a TA."""
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == user_id
    ).first()
    
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    
    tracker = get_tracker_for_ta(ta)
    learned_units = set(tracker.get_learned_units())
    
    # Get all teaching events
    sessions = db.query(TeachingSession).filter(
        TeachingSession.ta_instance_id == ta_id
    ).all()
    session_ids = [s.id for s in sessions]
    
    # Teaching statistics
    teach_events = db.query(TeachingEvent).filter(
        TeachingEvent.session_id.in_(session_ids)
    ).all() if session_ids else []
    
    total_teachings = len(teach_events)
    avg_quality_score = sum(
        (te.quality_score or 0) for te in teach_events
    ) / max(1, total_teachings)
    
    # Topics covered
    topics_covered = set()
    for te in teach_events:
        if te.topic_taught:
            topics_covered.add(te.topic_taught)
    
    # Test statistics
    test_attempts = db.query(TestAttempt).filter(
        TestAttempt.session_id.in_(session_ids)
    ).all() if session_ids else []
    
    total_tests = len(test_attempts)
    passed_tests = sum(1 for t in test_attempts if t.passed)
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    # Time analysis
    if teach_events:
        timestamps = [te.created_at for te in teach_events if te.created_at]
        if timestamps:
            first_activity = min(timestamps)
            last_activity = max(timestamps)
            study_duration_days = (last_activity - first_activity).days + 1
        else:
            study_duration_days = 0
    else:
        study_duration_days = 0
    
    # Gamification data
    gamification = db.query(GamificationProfile).filter(
        GamificationProfile.user_id == user_id
    ).first()
    
    # BKT state
    bkt_state = tracker.get_bkt_state()
    avg_mastery = sum(bkt_state.values()) / max(1, len(bkt_state))
    
    return {
        "student_info": {
            "user_id": user_id,
            "domain": ta.domain_id,
            "generated_at": datetime.utcnow().isoformat(),
        },
        "summary": {
            "total_concepts_learned": len(learned_units),
            "total_teaching_sessions": total_teachings,
            "total_tests_taken": total_tests,
            "test_pass_rate": round(pass_rate, 1),
            "average_teaching_quality": round(avg_quality_score, 2),
            "study_duration_days": study_duration_days,
        },
        "learning_progress": {
            "concepts_mastered": list(learned_units),
            "topics_covered": list(topics_covered),
            "average_mastery_probability": round(avg_mastery, 3),
            "knowledge_state": bkt_state,
        },
        "engagement": {
            "total_interactions": total_teachings + total_tests,
            "teaching_to_test_ratio": round(total_teachings / max(1, total_tests), 2),
            "average_quality_trend": _calculate_quality_trend(teach_events),
        },
        "gamification": {
            "points": gamification.xp if gamification else 0,
            "level": gamification.level if gamification else 1,
            "achievements_unlocked": len([a for a in (gamification.badges or []) if a.get("unlocked")]),
        } if gamification else None,
    }


def _calculate_quality_trend(teach_events: list) -> str:
    """Calculate if teaching quality is improving."""
    if len(teach_events) < 3:
        return "insufficient_data"
    
    sorted_events = sorted(teach_events, key=lambda x: x.created_at or datetime.min)
    
    first_half = sorted_events[:len(sorted_events)//2]
    second_half = sorted_events[len(sorted_events)//2:]
    
    first_avg = sum((te.quality_score or 0) for te in first_half) / max(1, len(first_half))
    second_avg = sum((te.quality_score or 0) for te in second_half) / max(1, len(second_half))
    
    if second_avg > first_avg * 1.1:
        return "improving"
    elif second_avg < first_avg * 0.9:
        return "declining"
    else:
        return "stable"


@router.get("/my-learning")
def get_my_learning_report(
    ta_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Generate a comprehensive learning report for the current user."""
    return _get_learning_analytics(ta_id, current_user.id, db)


@router.get("/export-json")
def export_report_json(
    ta_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Export learning report as JSON (for external analysis)."""
    report = _get_learning_analytics(ta_id, current_user.id, db)
    return {
        "export_format": "json",
        "export_timestamp": datetime.utcnow().isoformat(),
        "report": report,
    }


@router.get("/class-summary")
def get_class_summary(
    current_user: CurrentUser,
    db: DbSession,
):
    """Get summary statistics for all students (teacher view)."""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view class summaries")
    
    # Get all student TAs
    student_tas = db.query(TAInstance).join(User).filter(
        User.role == "student"
    ).all()
    
    domain_stats: dict[str, dict] = {}
    
    for ta in student_tas:
        domain = ta.domain_id
        if domain not in domain_stats:
            domain_stats[domain] = {
                "total_students": 0,
                "total_concepts_learned": [],
                "avg_test_pass_rate": [],
            }
        
        tracker = get_tracker_for_ta(ta)
        learned = len(tracker.get_learned_units())
        domain_stats[domain]["total_students"] += 1
        domain_stats[domain]["total_concepts_learned"].append(learned)
    
    # Calculate averages
    summary = {}
    for domain, stats in domain_stats.items():
        summary[domain] = {
            "total_students": stats["total_students"],
            "avg_concepts_learned": round(
                sum(stats["total_concepts_learned"]) / max(1, len(stats["total_concepts_learned"])), 1
            ),
        }
    
    return {
        "generated_at": datetime.utcnow().isoformat(),
        "class_summary": summary,
        "total_students": len(set(ta.user_id for ta in student_tas)),
    }
