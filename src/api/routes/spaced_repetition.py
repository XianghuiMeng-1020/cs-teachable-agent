"""Spaced Repetition API routes."""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import Optional

from src.api.deps import DbSession, CurrentUser
from src.core.spaced_repetition import (
    schedule_review,
    get_due_reviews,
    SpacedRepetitionScheduler,
    create_review_schedule_for_ta,
)
from src.api.domain_helpers import get_tracker_for_ta
from src.db.models import TAInstance

router = APIRouter(prefix="/api/spaced-repetition", tags=["spaced-repetition"])


@router.post("/schedule-review/{ta_id}")
def create_review_schedule(
    ta_id: int,
    data: dict,
    current_user = Depends(),
    db = Depends(),
):
    """Schedule a review for a knowledge unit."""
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == current_user.id
    ).first()
    
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    
    unit_id = data.get("unit_id")
    rating = data.get("rating", 3)  # Default to GOOD
    existing = data.get("existing_item")
    
    # Get BKT state
    tracker = get_tracker_for_ta(ta)
    p_know = tracker.get_bkt_state().get(unit_id, 0.5)
    
    result = schedule_review(unit_id, rating, existing, p_know)
    
    return result


@router.get("/due-reviews/{ta_id}")
def get_due_reviews_for_ta(
    ta_id: int,
    current_user = Depends(),
    db = Depends(),
):
    """Get all knowledge units due for review."""
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == current_user.id
    ).first()
    
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    
    # Get learned units
    tracker = get_tracker_for_ta(ta)
    learned_units = list(tracker.get_learned_units())
    bkt_state = tracker.get_bkt_state()
    
    # Get existing schedule from TA knowledge_state
    existing_schedule = ta.knowledge_state.get("review_schedule", []) if isinstance(ta.knowledge_state, dict) else []
    
    # Get unit definitions for names
    from src.api.domain_helpers import get_domain_adapter
    adapter = get_domain_adapter(ta.domain_id)
    kus = adapter.load_knowledge_units()
    unit_names = {u["id"]: u.get("name", u["id"]) for u in kus}
    
    # Create review items
    items = create_review_schedule_for_ta(ta, learned_units, unit_names, existing_schedule)
    
    # Get due items
    scheduler = SpacedRepetitionScheduler(bkt_p_know=bkt_state)
    due_items = scheduler.get_due_items(items)
    
    # Get retention stats
    stats = scheduler.calculate_retention_stats(items)
    
    return {
        "due_count": len(due_items),
        "due_items": [item.to_dict() for item in due_items],
        "retention_stats": stats,
    }


@router.get("/daily-plan/{ta_id}")
def get_daily_review_plan(
    ta_id: int,
    max_reviews: int = 20,
    current_user = Depends(),
    db = Depends(),
):
    """Get optimized daily review plan."""
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == current_user.id
    ).first()
    
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    
    # Get learned units
    tracker = get_tracker_for_ta(ta)
    learned_units = list(tracker.get_learned_units())
    bkt_state = tracker.get_bkt_state()
    
    # Get existing schedule
    existing_schedule = ta.knowledge_state.get("review_schedule", []) if isinstance(ta.knowledge_state, dict) else []
    
    # Get unit names
    from src.api.domain_helpers import get_domain_adapter
    adapter = get_domain_adapter(ta.domain_id)
    kus = adapter.load_knowledge_units()
    unit_names = {u["id"]: u.get("name", u["id"]) for u in kus}
    
    # Create items
    items = create_review_schedule_for_ta(ta, learned_units, unit_names, existing_schedule)
    
    # Generate plan
    scheduler = SpacedRepetitionScheduler(bkt_p_know=bkt_state)
    plan = scheduler.generate_daily_review_plan(items, max_reviews=max_reviews)
    
    return plan


@router.get("/retention-stats/{ta_id}")
def get_retention_statistics(
    ta_id: int,
    current_user = Depends(),
    db = Depends(),
):
    """Get memory retention statistics."""
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == current_user.id
    ).first()
    
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    
    tracker = get_tracker_for_ta(ta)
    learned_units = list(tracker.get_learned_units())
    bkt_state = tracker.get_bkt_state()
    
    # Get existing schedule
    existing_schedule = ta.knowledge_state.get("review_schedule", []) if isinstance(ta.knowledge_state, dict) else []
    
    # Get unit names
    from src.api.domain_helpers import get_domain_adapter
    adapter = get_domain_adapter(ta.domain_id)
    kus = adapter.load_knowledge_units()
    unit_names = {u["id"]: u.get("name", u["id"]) for u in kus}
    
    # Create items
    items = create_review_schedule_for_ta(ta, learned_units, unit_names, existing_schedule)
    
    # Calculate stats
    scheduler = SpacedRepetitionScheduler(bkt_p_know=bkt_state)
    stats = scheduler.calculate_retention_stats(items)
    
    # Add forgetting curve visualization data
    from src.core.spaced_repetition import ForgettingCurve
    
    curve_data = []
    avg_ease = stats.get("average_ease_factor", 2.5)
    forgetting = ForgettingCurve(
        initial_strength=avg_ease / 3,
        decay_rate=0.3
    )
    
    for day in [1, 3, 7, 14, 30, 60, 90]:
        curve_data.append({
            "day": day,
            "retention": round(forgetting.recall_probability(day) * 100, 1),
        })
    
    return {
        "statistics": stats,
        "forgetting_curve": curve_data,
        "total_learned": len(learned_units),
    }


@router.post("/rate/{ta_id}")
def rate_review(
    ta_id: int,
    data: dict,
    current_user = Depends(),
    db = Depends(),
):
    """Rate a review and update schedule."""
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == current_user.id
    ).first()
    
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    
    unit_id = data.get("unit_id")
    rating = data.get("rating")  # 1-4
    
    if not unit_id or not rating or not (1 <= rating <= 4):
        raise HTTPException(status_code=400, detail="Invalid unit_id or rating")
    
    # Get existing schedule
    existing_schedule = ta.knowledge_state.get("review_schedule", []) if isinstance(ta.knowledge_state, dict) else []
    existing = next((s for s in existing_schedule if s.get("unit_id") == unit_id), None)
    
    # Get BKT state
    tracker = get_tracker_for_ta(ta)
    p_know = tracker.get_bkt_state().get(unit_id, 0.5)
    
    # Schedule review
    result = schedule_review(unit_id, rating, existing, p_know)
    
    # Update TA knowledge_state
    if isinstance(ta.knowledge_state, dict):
        # Remove old entry if exists
        ta.knowledge_state["review_schedule"] = [
            s for s in existing_schedule if s.get("unit_id") != unit_id
        ]
        # Add updated entry
        ta.knowledge_state["review_schedule"].append(result)
    else:
        ta.knowledge_state = {"review_schedule": [result]}
    
    db.commit()
    
    return {
        "scheduled": result,
        "message": f"Next review scheduled for {result.get('next_review')}",
    }
