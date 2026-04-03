"""Adaptive Test Generation API routes."""

from fastapi import APIRouter, Depends, HTTPException
from src.api.deps import DbSession, CurrentUser
from src.core.adaptive_test_generator import generate_adaptive_test_for_ta
from src.db.models import TAInstance

router = APIRouter(prefix="/api/adaptive-test", tags=["adaptive-test"])


@router.post("/generate/{ta_id}")
def generate_adaptive_test(
    ta_id: int,
    num_questions: int = 5,
    current_user: CurrentUser,
    db: DbSession,
):
    """Generate a personalized adaptive test for the TA."""
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == current_user.id
    ).first()
    
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    
    test = generate_adaptive_test_for_ta(ta, num_questions=num_questions)
    
    return test


@router.get("/question-types")
def get_question_types():
    """Get available question types and difficulty levels."""
    return {
        "difficulty_levels": [
            {"value": 1, "label": "Easy", "description": "Basic concept recall"},
            {"value": 2, "label": "Medium", "description": "Application and understanding"},
            {"value": 3, "label": "Hard", "description": "Analysis and problem-solving"},
            {"value": 4, "label": "Expert", "description": "Complex design and optimization"},
        ],
        "question_types": [
            {"value": "conceptual", "label": "Conceptual", "description": "Tests understanding of core concepts"},
            {"value": "application", "label": "Application", "description": "Requires applying knowledge to solve problems"},
            {"value": "analysis", "label": "Analysis", "description": "Requires analyzing and reasoning about code"},
        ],
    }
