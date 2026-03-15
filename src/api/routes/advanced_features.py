"""Advanced features API routes."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from src.api.deps import DbSession, CurrentUser
from src.core.peer_help_matcher import match_peer_help
from src.core.emotion_aware_teaching import analyze_student_emotion
from src.core.ai_code_reviewer import review_student_code
from src.core.advanced_achievement_system import get_student_achievements
from src.core.cross_domain_transfer import analyze_cross_domain_transfer

router = APIRouter(prefix="/api/advanced", tags=["advanced"])


@router.post("/peer-help/match")
def find_peer_help(
    request_data: dict,
    helper_profiles: List[dict],
    db: DbSession,
    user: CurrentUser,
):
    """Find matching helpers for a help request."""
    return match_peer_help(request_data, helper_profiles)


@router.post("/emotion/analyze")
def analyze_emotion(
    message: str,
    student_id: int,
    recent_performance: float = 0.5,
    consecutive_errors: int = 0,
    session_minutes: int = 0,
    db: DbSession = None,
    user: CurrentUser = None,
):
    """Analyze student emotion from message."""
    return analyze_student_emotion(
        message, student_id, recent_performance, consecutive_errors, session_minutes
    )


@router.post("/code-review")
def review_code(
    code: str,
    student_level: str = "beginner",
    db: DbSession = None,
    user: CurrentUser = None,
):
    """Review student code with AI."""
    return review_student_code(code, student_level)


@router.get("/achievements/{student_id}")
def get_achievements(
    student_id: int,
    db: DbSession,
    user: CurrentUser,
):
    """Get student achievements."""
    if user.id != student_id and not user.is_teacher:
        raise HTTPException(403, "Not authorized")
    
    # Mock progress data
    progress_data = {
        "lessons_completed": 15,
        "total_lessons": 50,
        "concepts_mastered": 12,
        "lines_of_code": 500,
        "help_given": 3,
        "current_streak": 7,
        "total_points": 450,
    }
    
    return get_student_achievements(student_id, progress_data)


@router.post("/transfer-analysis")
def analyze_transfer(
    student_id: int,
    source_domain: str,
    target_domain: str,
    source_mastery: Dict[str, float],
    db: DbSession = None,
    user: CurrentUser = None,
):
    """Analyze cross-domain knowledge transfer."""
    return analyze_cross_domain_transfer(
        student_id, source_domain, target_domain, source_mastery
    )
