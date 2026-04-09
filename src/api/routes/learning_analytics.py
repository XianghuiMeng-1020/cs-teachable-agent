"""Learning analytics API routes."""

from fastapi import APIRouter, Body, HTTPException
from typing import List, Optional
from src.api.deps import DbSession, CurrentUser
from src.core.learning_pace_detector import detect_learning_pace
from src.core.cognitive_load_monitor import monitor_student_cognitive_load
from src.core.concept_relation_inference import infer_concept_relations

router = APIRouter(prefix="/api/learning-analytics", tags=["learning-analytics"])


@router.post("/pace-detection/{student_id}")
def analyze_learning_pace(
    student_id: int,
    db: DbSession,
    user: CurrentUser,
    session_history: List[dict] = Body(default_factory=list),
):
    """Analyze student's learning pace and provide recommendations."""
    if user.id != student_id and not user.role == "teacher":
        raise HTTPException(403, "Not authorized")
    
    return detect_learning_pace(student_id, session_history)


@router.post("/cognitive-load/{student_id}")
def assess_cognitive_load(
    student_id: int,
    db: DbSession,
    user: CurrentUser,
    session_data: dict = Body(default_factory=dict),
    context_history: Optional[List[dict]] = Body(default=None),
):
    """Assess current cognitive load and provide recommendations."""
    if user.id != student_id and not user.role == "teacher":
        raise HTTPException(403, "Not authorized")
    
    return monitor_student_cognitive_load(
        student_id,
        session_data,
        context_history or []
    )


@router.post("/concept-relations/infer")
def infer_concept_relationships(
    db: DbSession,
    user: CurrentUser,
    knowledge_units: List[dict] = Body(default_factory=list),
    learning_sequences: Optional[List[List[str]]] = Body(default=None),
    descriptions: Optional[dict] = Body(default=None),
):
    """Infer concept relationships from curriculum and learning data."""
    return infer_concept_relations(
        knowledge_units,
        learning_sequences or [],
        descriptions or {}
    )
