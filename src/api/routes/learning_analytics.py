"""Learning analytics API routes."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from src.api.deps import DbSession, CurrentUser
from src.core.learning_pace_detector import detect_learning_pace
from src.core.cognitive_load_monitor import monitor_student_cognitive_load
from src.core.concept_relation_inference import infer_concept_relations

router = APIRouter(prefix="/api/learning-analytics", tags=["learning-analytics"])


@router.post("/pace-detection/{student_id}")
def analyze_learning_pace(
    student_id: int,
    session_history: List[dict],
    db: DbSession,
    user: CurrentUser,
):
    """Analyze student's learning pace and provide recommendations."""
    if user.id != student_id and not user.is_teacher:
        raise HTTPException(403, "Not authorized")
    
    return detect_learning_pace(student_id, session_history)


@router.post("/cognitive-load/{student_id}")
def assess_cognitive_load(
    student_id: int,
    session_data: dict,
    context_history: Optional[List[dict]] = None,
    db: DbSession = None,
    user: CurrentUser = None,
):
    """Assess current cognitive load and provide recommendations."""
    if user.id != student_id and not user.is_teacher:
        raise HTTPException(403, "Not authorized")
    
    return monitor_student_cognitive_load(
        student_id,
        session_data,
        context_history or []
    )


@router.post("/concept-relations/infer")
def infer_concept_relationships(
    knowledge_units: List[dict],
    learning_sequences: Optional[List[List[str]]] = None,
    descriptions: Optional[dict] = None,
    db: DbSession = None,
    user: CurrentUser = None,
):
    """Infer concept relationships from curriculum and learning data."""
    return infer_concept_relations(
        knowledge_units,
        learning_sequences or [],
        descriptions or {}
    )
