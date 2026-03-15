"""Gamification: points, level, achievements for current user."""

from fastapi import APIRouter, Depends

from sqlalchemy import func

from src.api.deps import DbSession, CurrentUser
from src.db.models import TAInstance, TeachingSession, TeachingEvent, TestAttempt
from src.core.gamification_engine import (
    compute_points,
    level_from_points,
    all_achievements_with_status,
)

router = APIRouter(prefix="/api/gamification", tags=["gamification"])


@router.get("/me")
def get_my_gamification(current_user: CurrentUser, db: DbSession):
    """Return points, level, and achievements for the current user (student)."""
    ta_ids = [r.id for r in db.query(TAInstance.id).filter(TAInstance.user_id == current_user.id).all()]
    if not ta_ids:
        return {
            "points": 0,
            "level": 1,
            "teach_count": 0,
            "test_attempt_count": 0,
            "test_pass_count": 0,
            "achievements": [],
        }
    session_ids = [
        r.id for r in db.query(TeachingSession.id).filter(TeachingSession.ta_instance_id.in_(ta_ids)).all()
    ]
    if not session_ids:
        return {
            "points": 0,
            "level": 1,
            "teach_count": 0,
            "test_attempt_count": 0,
            "test_pass_count": 0,
            "achievements": [],
        }
    teach_count = (
        db.query(func.count(TeachingEvent.id))
        .filter(TeachingEvent.session_id.in_(session_ids))
        .scalar() or 0
    )
    test_attempts = (
        db.query(TestAttempt).filter(TestAttempt.session_id.in_(session_ids)).all()
    )
    test_attempt_count = len(test_attempts)
    test_pass_count = sum(1 for t in test_attempts if t.passed)
    points = compute_points(teach_count, test_attempt_count, test_pass_count)
    level = level_from_points(points)
    achievements = all_achievements_with_status(teach_count, test_pass_count, level)
    return {
        "points": points,
        "level": level,
        "teach_count": teach_count,
        "test_attempt_count": test_attempt_count,
        "test_pass_count": test_pass_count,
        "achievements": achievements,
    }
