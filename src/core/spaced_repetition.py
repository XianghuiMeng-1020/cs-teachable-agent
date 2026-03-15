"""
Spaced Repetition System

Implements evidence-based spaced repetition algorithms for optimal learning retention.

Algorithms:
- SM-2 (SuperMemo-2): Classic spaced repetition
- Modified SM-2 with BKT integration: Adapts to knowledge state
- Forgetting curve prediction: Estimates optimal review time

Research Applications:
- Memory retention studies
- Optimal learning schedule optimization
- Personalized review timing
"""

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum


class ReviewRating(Enum):
    """User's self-assessment of recall quality."""
    AGAIN = 1  # Complete blackout
    HARD = 2   # Incorrect response, remembered after seeing answer
    GOOD = 3   # Correct with hesitation
    EASY = 4   # Perfect response


@dataclass
class ReviewItem:
    """A knowledge unit scheduled for review."""
    unit_id: str
    unit_name: str
    ease_factor: float = 2.5  # SM-2 ease factor
    interval_days: float = 0  # Days until next review
    repetitions: int = 0  # Number of successful reviews
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None
    review_history: list[dict] = field(default_factory=list)
    
    # Enhanced tracking
    total_reviews: int = 0
    successful_reviews: int = 0
    average_rating: float = 0.0
    forgetting_rate: float = 0.3  # Estimated forgetting rate (0-1)
    
    def to_dict(self) -> dict:
        return {
            "unit_id": self.unit_id,
            "unit_name": self.unit_name,
            "ease_factor": round(self.ease_factor, 2),
            "interval_days": round(self.interval_days, 1),
            "repetitions": self.repetitions,
            "last_reviewed": self.last_reviewed.isoformat() if self.last_reviewed else None,
            "next_review": self.next_review.isoformat() if self.next_review else None,
            "total_reviews": self.total_reviews,
            "successful_reviews": self.successful_reviews,
            "average_rating": round(self.average_rating, 2),
            "forgetting_rate": round(self.forgetting_rate, 3),
        }


@dataclass
class ForgettingCurve:
    """Models the forgetting curve for a knowledge item."""
    initial_strength: float  # Memory strength after learning (0-1)
    decay_rate: float  # How fast memory fades
    
    def recall_probability(self, days_since_review: float) -> float:
        """
        Calculate probability of recall after N days.
        Uses exponential decay model: R = e^(-t/S)
        where t is time, S is memory strength
        """
        if days_since_review <= 0:
            return 1.0
        
        # Exponential forgetting curve
        # R = e^(-t/S) where S is the stability parameter
        stability = self.initial_strength / self.decay_rate
        recall_prob = math.exp(-days_since_review / max(1, stability))
        
        return max(0.0, min(1.0, recall_prob))
    
    def optimal_review_time(
        self,
        target_retention: float = 0.9,
        max_days: int = 365
    ) -> int:
        """
        Calculate optimal review time to maintain target retention.
        
        Args:
            target_retention: Desired recall probability (default 90%)
            max_days: Maximum interval to consider
        
        Returns:
            Recommended days until next review
        """
        # Solve for t: target = e^(-t/S)
        # ln(target) = -t/S
        # t = -S * ln(target)
        stability = self.initial_strength / self.decay_rate
        
        if target_retention >= 1.0:
            return 1
        
        days = -stability * math.log(target_retention)
        return min(max_days, max(1, int(round(days))))


class SpacedRepetitionScheduler:
    """SM-2 based spaced repetition with BKT integration."""
    
    # SM-2 constants
    MIN_EASE_FACTOR = 1.3
    DEFAULT_EASE_FACTOR = 2.5
    
    # Interval multipliers based on rating
    INTERVAL_MULTIPLIERS = {
        ReviewRating.AGAIN: 0.0,  # Reset
        ReviewRating.HARD: 1.2,
        ReviewRating.GOOD: 1.0,
        ReviewRating.EASY: 1.3,
    }
    
    # Ease factor adjustments
    EASE_ADJUSTMENTS = {
        ReviewRating.AGAIN: -0.8,
        ReviewRating.HARD: -0.15,
        ReviewRating.GOOD: 0.0,
        ReviewRating.EASY: 0.15,
    }
    
    def __init__(self, bkt_p_know: Optional[dict] = None):
        """
        Initialize scheduler with optional BKT knowledge state.
        
        Args:
            bkt_p_know: Dictionary mapping unit_id to p_know from BKT
        """
        self.bkt_p_know = bkt_p_know or {}
    
    def schedule_review(
        self,
        item: ReviewItem,
        rating: ReviewRating,
        review_date: Optional[datetime] = None
    ) -> ReviewItem:
        """
        Schedule next review based on SM-2 algorithm with BKT enhancement.
        
        Args:
            item: The review item being scheduled
            rating: User's performance rating
            review_date: When review occurred (default: now)
        
        Returns:
            Updated ReviewItem with new schedule
        """
        if review_date is None:
            review_date = datetime.utcnow()
        
        # Update review history
        item.review_history.append({
            "date": review_date.isoformat(),
            "rating": rating.value,
            "interval_before": item.interval_days,
        })
        
        item.total_reviews += 1
        item.last_reviewed = review_date
        
        # Calculate forgetting rate from review pattern
        if item.total_reviews > 1:
            # Estimate forgetting rate from performance
            success_rate = item.successful_reviews / item.total_reviews
            item.forgetting_rate = 0.3 + (1 - success_rate) * 0.4
        
        # Handle failed review (AGAIN)
        if rating == ReviewRating.AGAIN:
            item.repetitions = 0
            item.interval_days = 1  # Review tomorrow
            item.ease_factor = max(
                self.MIN_EASE_FACTOR,
                item.ease_factor + self.EASE_ADJUSTMENTS[rating]
            )
        else:
            # Successful review
            item.successful_reviews += 1
            
            # Update ease factor
            item.ease_factor = max(
                self.MIN_EASE_FACTOR,
                item.ease_factor + self.EASE_ADJUSTMENTS[rating]
            )
            
            # Calculate interval
            if item.repetitions == 0:
                # First successful review
                if rating == ReviewRating.HARD:
                    item.interval_days = 1
                elif rating == ReviewRating.GOOD:
                    item.interval_days = 3
                else:  # EASY
                    item.interval_days = 4
            elif item.repetitions == 1:
                item.interval_days = 6 * self.INTERVAL_MULTIPLIERS[rating]
            else:
                # Subsequent reviews: multiply by ease factor
                multiplier = self.INTERVAL_MULTIPLIERS[rating]
                item.interval_days = item.interval_days * item.ease_factor * multiplier
            
            item.repetitions += 1
        
        # Apply BKT adjustment if available
        p_know = self.bkt_p_know.get(item.unit_id, 0.5)
        if p_know < 0.7:
            # Lower mastery = more frequent review
            item.interval_days *= 0.7
        elif p_know > 0.9 and rating == ReviewRating.EASY:
            # High mastery + easy = can extend interval
            item.interval_days *= 1.2
        
        # Cap maximum interval
        item.interval_days = min(365, item.interval_days)
        
        # Calculate next review date
        item.next_review = review_date + timedelta(days=item.interval_days)
        
        # Update average rating
        total_rating = sum(r["rating"] for r in item.review_history)
        item.average_rating = total_rating / len(item.review_history)
        
        return item
    
    def get_due_items(
        self,
        items: list[ReviewItem],
        date: Optional[datetime] = None
    ) -> list[ReviewItem]:
        """
        Get items due for review on or before given date.
        
        Args:
            items: List of all review items
            date: Date to check (default: now)
        
        Returns:
            List of items due for review
        """
        if date is None:
            date = datetime.utcnow()
        
        due = []
        for item in items:
            if item.next_review is None:
                # New items that haven't been reviewed
                due.append(item)
            elif item.next_review <= date:
                due.append(item)
        
        # Sort by priority (lower p_know = higher priority)
        due.sort(key=lambda i: (
            self.bkt_p_know.get(i.unit_id, 0.5),
            i.next_review or datetime.min
        ))
        
        return due
    
    def calculate_retention_stats(
        self,
        items: list[ReviewItem]
    ) -> dict:
        """
        Calculate memory retention statistics.
        
        Returns:
            Dictionary with retention metrics
        """
        if not items:
            return {"message": "No review data available"}
        
        total_items = len(items)
        due_items = len(self.get_due_items(items))
        
        # Calculate average metrics
        avg_ease = sum(i.ease_factor for i in items) / total_items
        avg_interval = sum(i.interval_days for i in items) / total_items
        
        # Forgetting curve analysis
        forgetting_curve = ForgettingCurve(
            initial_strength=avg_ease / 3,  # Rough estimate
            decay_rate=0.3
        )
        
        # Predict retention at different intervals
        retention_predictions = {
            "1_day": round(forgetting_curve.recall_probability(1), 3),
            "7_days": round(forgetting_curve.recall_probability(7), 3),
            "30_days": round(forgetting_curve.recall_probability(30), 3),
        }
        
        # Items by repetition count
        repetition_distribution = {}
        for i in items:
            bucket = min(i.repetitions, 5)  # Group 5+ together
            repetition_distribution[bucket] = repetition_distribution.get(bucket, 0) + 1
        
        return {
            "total_scheduled": total_items,
            "due_now": due_items,
            "up_to_date": total_items - due_items,
            "average_ease_factor": round(avg_ease, 2),
            "average_interval_days": round(avg_interval, 1),
            "predicted_retention": retention_predictions,
            "repetition_distribution": repetition_distribution,
            "retention_health": "good" if avg_ease > 2.0 else "needs_improvement",
        }
    
    def generate_daily_review_plan(
        self,
        items: list[ReviewItem],
        max_reviews: int = 20,
        date: Optional[datetime] = None
    ) -> dict:
        """
        Generate an optimal daily review plan.
        
        Args:
            items: All review items
            max_reviews: Maximum reviews to schedule
            date: Target date
        
        Returns:
            Review plan with prioritized items
        """
        if date is None:
            date = datetime.utcnow()
        
        # Get due items
        due = self.get_due_items(items, date)
        
        # Priority scoring
        def priority_score(item: ReviewItem) -> float:
            score = 0.0
            
            # Higher priority if overdue
            if item.next_review:
                days_overdue = (date - item.next_review).days
                score += days_overdue * 10
            
            # Higher priority if low mastery
            p_know = self.bkt_p_know.get(item.unit_id, 0.5)
            score += (1 - p_know) * 20
            
            # Higher priority if fewer repetitions
            score += (5 - min(item.repetitions, 5)) * 5
            
            # Lower ease factor = higher priority
            score += (3.0 - item.ease_factor) * 10
            
            return score
        
        # Sort by priority
        prioritized = sorted(due, key=priority_score, reverse=True)
        
        # Select top items
        selected = prioritized[:max_reviews]
        
        # Calculate estimated time
        est_time_per_review = 2  # minutes
        total_estimated_time = len(selected) * est_time_per_review
        
        return {
            "date": date.isoformat(),
            "total_due": len(due),
            "selected_for_review": len(selected),
            "estimated_minutes": total_estimated_time,
            "items": [item.to_dict() for item in selected],
            "skipped": len(due) - len(selected),
            "optimization": "Prioritized by overdue days, mastery level, and repetition count",
        }


def create_review_schedule_for_ta(
    ta,
    learned_units: list[str],
    unit_names: dict[str, str],
    existing_schedule: Optional[list[dict]] = None
) -> list[ReviewItem]:
    """
    Create or update spaced repetition schedule for a TA.
    
    This is the main API-facing function.
    """
    from src.api.domain_helpers import get_tracker_for_ta
    
    tracker = get_tracker_for_ta(ta)
    bkt_state = tracker.get_bkt_state()
    
    # Initialize scheduler
    scheduler = SpacedRepetitionScheduler(bkt_p_know=bkt_state)
    
    # Create review items
    items = []
    for unit_id in learned_units:
        # Check if already in schedule
        existing = None
        if existing_schedule:
            existing = next((s for s in existing_schedule if s.get("unit_id") == unit_id), None)
        
        if existing:
            # Restore from existing
            item = ReviewItem(
                unit_id=unit_id,
                unit_name=existing.get("unit_name", unit_names.get(unit_id, unit_id)),
                ease_factor=existing.get("ease_factor", 2.5),
                interval_days=existing.get("interval_days", 0),
                repetitions=existing.get("repetitions", 0),
                last_reviewed=datetime.fromisoformat(existing["last_reviewed"]) if existing.get("last_reviewed") else None,
                next_review=datetime.fromisoformat(existing["next_review"]) if existing.get("next_review") else None,
                total_reviews=existing.get("total_reviews", 0),
                successful_reviews=existing.get("successful_reviews", 0),
            )
        else:
            # Create new item
            item = ReviewItem(
                unit_id=unit_id,
                unit_name=unit_names.get(unit_id, unit_id),
            )
        
        items.append(item)
    
    return items


# Convenience functions for API

def schedule_review(
    unit_id: str,
    rating_value: int,
    existing_item: Optional[dict] = None,
    bkt_p_know: Optional[float] = None
) -> dict:
    """Schedule a single review - API convenience function."""
    rating = ReviewRating(rating_value)
    
    if existing_item:
        item = ReviewItem(
            unit_id=existing_item["unit_id"],
            unit_name=existing_item.get("unit_name", unit_id),
            ease_factor=existing_item.get("ease_factor", 2.5),
            interval_days=existing_item.get("interval_days", 0),
            repetitions=existing_item.get("repetitions", 0),
        )
    else:
        item = ReviewItem(unit_id=unit_id, unit_name=unit_id)
    
    scheduler = SpacedRepetitionScheduler({unit_id: bkt_p_know} if bkt_p_know else {})
    updated = scheduler.schedule_review(item, rating)
    
    return updated.to_dict()


def get_due_reviews(
    schedule: list[dict],
    bkt_state: dict[str, float],
    date: Optional[datetime] = None
) -> list[dict]:
    """Get all due reviews - API convenience function."""
    scheduler = SpacedRepetitionScheduler(bkt_p_know=bkt_state)
    
    items = [
        ReviewItem(
            unit_id=s["unit_id"],
            unit_name=s.get("unit_name", s["unit_id"]),
            ease_factor=s.get("ease_factor", 2.5),
            interval_days=s.get("interval_days", 0),
            repetitions=s.get("repetitions", 0),
            last_reviewed=datetime.fromisoformat(s["last_reviewed"]) if s.get("last_reviewed") else None,
            next_review=datetime.fromisoformat(s["next_review"]) if s.get("next_review") else None,
        )
        for s in schedule
    ]
    
    due = scheduler.get_due_items(items, date)
    return [item.to_dict() for item in due]
