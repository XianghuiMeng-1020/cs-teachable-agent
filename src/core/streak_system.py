"""
Learning Streak System

Gamified learning continuity tracking with research-backed motivation principles.

Features:
- Daily streak tracking
- Streak freeze (allow occasional misses)
- Milestone rewards
- Social streak comparison
- Streak recovery mechanisms
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import json


@dataclass
class StreakDay:
    """Record of a single day's learning activity."""
    date: str  # ISO format date
    activity_count: int
    concepts_learned: int
    tests_completed: int
    total_learning_time_minutes: int
    was_active: bool


@dataclass
class StreakMilestone:
    """Milestone achievement."""
    days_required: int
    name: str
    description: str
    reward_points: int
    badge_icon: str


@dataclass
class StreakData:
    """Complete streak information for a user."""
    user_id: int
    current_streak: int = 0
    longest_streak: int = 0
    total_active_days: int = 0
    streak_freezes_used: int = 0
    streak_freezes_remaining: int = 2
    last_active_date: Optional[str] = None
    history: list[StreakDay] = field(default_factory=list)
    milestones_achieved: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "total_active_days": self.total_active_days,
            "streak_freezes_used": self.streak_freezes_used,
            "streak_freezes_remaining": self.streak_freezes_remaining,
            "last_active_date": self.last_active_date,
            "history": [self._day_to_dict(d) for d in self.history[-30:]],  # Last 30 days
            "milestones_achieved": self.milestones_achieved,
        }
    
    @staticmethod
    def _day_to_dict(day: StreakDay) -> dict:
        return {
            "date": day.date,
            "activity_count": day.activity_count,
            "concepts_learned": day.concepts_learned,
            "tests_completed": day.tests_completed,
            "total_learning_time_minutes": day.total_learning_time_minutes,
            "was_active": day.was_active,
        }


# Predefined milestones
STREAK_MILESTONES = [
    StreakMilestone(3, "Getting Started", "3-day learning streak!", 50, "🔥"),
    StreakMilestone(7, "Week Warrior", "One week of continuous learning!", 100, "⚡"),
    StreakMilestone(14, "Two Week Wonder", "Two weeks of dedication!", 200, "🌟"),
    StreakMilestone(21, "21-Day Habit", "Learning is now a habit!", 300, "🎯"),
    StreakMilestone(30, "Monthly Master", "A full month of learning!", 500, "🏆"),
    StreakMilestone(60, "Double Month", "Two months of consistency!", 800, "💎"),
    StreakMilestone(100, "Century Club", "100 days of learning!", 1500, "👑"),
    StreakMilestone(365, "Year of Growth", "A full year of continuous learning!", 5000, "🌈"),
]


class StreakSystem:
    """Manages learning streaks and gamification."""
    
    # Minimum activity to count as "active" day
    MIN_ACTIVITY_COUNT = 1
    MIN_LEARNING_TIME_MINUTES = 5
    
    def __init__(self):
        pass
    
    def check_and_update_streak(
        self,
        streak_data: StreakData,
        today_activity: dict,
    ) -> StreakData:
        """
        Check if user maintains streak and update accordingly.
        
        Args:
            streak_data: Current streak data
            today_activity: Today's activity summary
        
        Returns:
            Updated streak data
        """
        today = datetime.utcnow().date()
        today_str = today.isoformat()
        
        # Check if already recorded today
        if streak_data.last_active_date == today_str:
            return streak_data
        
        is_active_today = (
            today_activity.get("activity_count", 0) >= self.MIN_ACTIVITY_COUNT or
            today_activity.get("total_learning_time_minutes", 0) >= self.MIN_LEARNING_TIME_MINUTES
        )
        
        if not is_active_today:
            # No activity today - check if we need to use a freeze
            if streak_data.last_active_date:
                last_date = datetime.fromisoformat(streak_data.last_active_date).date()
                days_diff = (today - last_date).days
                
                if days_diff == 1:
                    # Missed yesterday but active today - check for freeze
                    if streak_data.streak_freezes_remaining > 0:
                        streak_data.streak_freezes_remaining -= 1
                        streak_data.streak_freezes_used += 1
                        # Streak continues via freeze
                    else:
                        # Streak broken
                        streak_data.current_streak = 1 if is_active_today else 0
                elif days_diff > 1:
                    # Streak already broken before today
                    streak_data.current_streak = 1 if is_active_today else 0
        else:
            # Active today
            if streak_data.last_active_date:
                last_date = datetime.fromisoformat(streak_data.last_active_date).date()
                days_diff = (today - last_date).days
                
                if days_diff == 1:
                    # Consecutive day - increment streak
                    streak_data.current_streak += 1
                elif days_diff > 1:
                    # Gap - check if streak freeze applies
                    if days_diff == 2 and streak_data.streak_freezes_remaining > 0:
                        streak_data.streak_freezes_remaining -= 1
                        streak_data.streak_freezes_used += 1
                        streak_data.current_streak += 1  # Continue with freeze
                    else:
                        streak_data.current_streak = 1
            else:
                # First activity ever
                streak_data.current_streak = 1
        
        # Update stats
        if is_active_today:
            streak_data.last_active_date = today_str
            streak_data.total_active_days += 1
            
            # Record day
            streak_data.history.append(StreakDay(
                date=today_str,
                activity_count=today_activity.get("activity_count", 0),
                concepts_learned=today_activity.get("concepts_learned", 0),
                tests_completed=today_activity.get("tests_completed", 0),
                total_learning_time_minutes=today_activity.get("total_learning_time_minutes", 0),
                was_active=True,
            ))
        
        # Update longest streak
        if streak_data.current_streak > streak_data.longest_streak:
            streak_data.longest_streak = streak_data.current_streak
        
        # Check milestones
        new_milestones = self._check_milestones(streak_data)
        streak_data.milestones_achieved.extend(new_milestones)
        
        # Replenish freezes periodically (every 7 days of streak)
        if streak_data.current_streak > 0 and streak_data.current_streak % 7 == 0:
            streak_data.streak_freezes_remaining = min(
                2,
                streak_data.streak_freezes_remaining + 1
            )
        
        return streak_data
    
    def _check_milestones(self, streak_data: StreakData) -> list[str]:
        """Check for newly achieved milestones."""
        new_milestones = []
        
        for milestone in STREAK_MILESTONES:
            if (
                streak_data.current_streak >= milestone.days_required and
                milestone.name not in streak_data.milestones_achieved
            ):
                new_milestones.append(milestone.name)
        
        return new_milestones
    
    def get_next_milestone(self, current_streak: int) -> Optional[StreakMilestone]:
        """Get the next milestone to achieve."""
        for milestone in STREAK_MILESTONES:
            if milestone.days_required > current_streak:
                return milestone
        return None
    
    def calculate_streak_risk(
        self,
        streak_data: StreakData,
        last_activity_date: Optional[str] = None,
    ) -> dict:
        """
        Calculate risk of losing streak.
        
        Returns risk assessment with recommendations.
        """
        today = datetime.utcnow().date()
        
        if not last_activity_date:
            return {
                "risk_level": "none",
                "days_until_break": None,
                "message": "No active streak",
                "recommendation": "Start learning to build a streak!",
            }
        
        last_date = datetime.fromisoformat(last_activity_date).date()
        days_since = (today - last_date).days
        
        if days_since == 0:
            return {
                "risk_level": "none",
                "days_until_break": 1,
                "message": "Streak safe - active today",
                "recommendation": "Great job! Come back tomorrow to continue.",
            }
        elif days_since == 1:
            risk = "high" if streak_data.streak_freezes_remaining == 0 else "medium"
            return {
                "risk_level": risk,
                "days_until_break": 0,
                "message": f"Streak expires today! {streak_data.streak_freezes_remaining} freezes remaining",
                "recommendation": "Study now to maintain your streak!",
            }
        else:
            return {
                "risk_level": "broken",
                "days_until_break": None,
                "message": "Streak already broken",
                "recommendation": "Start a new streak today!",
            }
    
    def get_streak_statistics(self, streak_data: StreakData) -> dict:
        """Get detailed streak statistics."""
        if not streak_data.history:
            return {"message": "No streak data available"}
        
        # Calculate weekly average
        recent_days = streak_data.history[-7:]
        avg_activity = sum(d.activity_count for d in recent_days) / max(1, len(recent_days))
        avg_time = sum(d.total_learning_time_minutes for d in recent_days) / max(1, len(recent_days))
        
        # Find best day
        best_day = max(streak_data.history, key=lambda d: d.activity_count)
        
        # Calculate consistency score
        last_30 = streak_data.history[-30:]
        active_days_30 = sum(1 for d in last_30 if d.was_active)
        consistency = (active_days_30 / 30) * 100
        
        return {
            "current_streak": streak_data.current_streak,
            "longest_streak": streak_data.longest_streak,
            "total_active_days": streak_data.total_active_days,
            "consistency_score": round(consistency, 1),
            "weekly_average": {
                "activities": round(avg_activity, 1),
                "minutes": round(avg_time, 1),
            },
            "best_day": {
                "date": best_day.date,
                "activities": best_day.activity_count,
            },
            "freezes_remaining": streak_data.streak_freezes_remaining,
            "milestones_count": len(streak_data.milestones_achieved),
        }
    
    def get_weekly_streak_calendar(
        self,
        streak_data: StreakData,
        weeks: int = 4,
    ) -> list[dict]:
        """Generate streak calendar data for visualization."""
        today = datetime.utcnow().date()
        calendar = []
        
        # Create lookup for history
        history_dict = {d.date: d for d in streak_data.history}
        
        for week in range(weeks):
            week_data = []
            for day in range(7):
                date = today - timedelta(days=week * 7 + day)
                date_str = date.isoformat()
                
                day_data = history_dict.get(date_str)
                
                week_data.append({
                    "date": date_str,
                    "day_name": date.strftime("%a"),
                    "is_today": date == today,
                    "was_active": day_data.was_active if day_data else False,
                    "activity_count": day_data.activity_count if day_data else 0,
                    "learning_time": day_data.total_learning_time_minutes if day_data else 0,
                })
            
            calendar.append({
                "week": week,
                "days": list(reversed(week_data)),  # Oldest first
            })
        
        return list(reversed(calendar))  # Most recent week first


def create_or_update_streak(
    user_id: int,
    existing_data: Optional[dict],
    today_activity: dict,
) -> StreakData:
    """
    Main API-facing function to update streak.
    
    Args:
        user_id: User ID
        existing_data: Existing streak data from database
        today_activity: Today's activity metrics
    
    Returns:
        Updated StreakData
    """
    system = StreakSystem()
    
    # Create or restore StreakData
    if existing_data:
        streak_data = StreakData(
            user_id=user_id,
            current_streak=existing_data.get("current_streak", 0),
            longest_streak=existing_data.get("longest_streak", 0),
            total_active_days=existing_data.get("total_active_days", 0),
            streak_freezes_used=existing_data.get("streak_freezes_used", 0),
            streak_freezes_remaining=existing_data.get("streak_freezes_remaining", 2),
            last_active_date=existing_data.get("last_active_date"),
            history=[StreakDay(**d) for d in existing_data.get("history", [])],
            milestones_achieved=existing_data.get("milestones_achieved", []),
        )
    else:
        streak_data = StreakData(user_id=user_id)
    
    # Update streak
    updated = system.check_and_update_streak(streak_data, today_activity)
    
    return updated


def get_streak_summary(streak_data: StreakData) -> dict:
    """Get concise streak summary for display."""
    system = StreakSystem()
    
    next_milestone = system.get_next_milestone(streak_data.current_streak)
    risk = system.calculate_streak_risk(streak_data, streak_data.last_active_date)
    
    return {
        "current_streak": streak_data.current_streak,
        "longest_streak": streak_data.longest_streak,
        "freezes_remaining": streak_data.streak_freezes_remaining,
        "next_milestone": {
            "name": next_milestone.name if next_milestone else None,
            "days_required": next_milestone.days_required if next_milestone else None,
            "days_to_go": (next_milestone.days_required - streak_data.current_streak) if next_milestone else None,
        },
        "risk_assessment": risk,
        "is_active_today": streak_data.last_active_date == datetime.utcnow().date().isoformat(),
    }
