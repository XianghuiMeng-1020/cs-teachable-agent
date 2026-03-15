"""
Advanced Achievement System

Gamified achievement system with badges, titles, and progression.
Enhances motivation through recognition and rewards.

Research Applications:
- Gamification in education
- Motivation and engagement
- Progress visualization
- Competency recognition
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from datetime import datetime, timedelta
import json


class AchievementTier(Enum):
    """Achievement rarity tiers."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"
    LEGENDARY = "legendary"


class AchievementCategory(Enum):
    """Categories of achievements."""
    LEARNING = "learning"
    PRACTICE = "practice"
    MASTERY = "mastery"
    SOCIAL = "social"
    CHALLENGE = "challenge"
    SPECIAL = "special"


@dataclass
class Badge:
    """Achievement badge."""
    id: str
    name: str
    description: str
    icon: str
    tier: AchievementTier
    category: AchievementCategory
    points: int
    criteria: Dict
    unlocked_at: Optional[str] = None
    progress: float = 0.0


@dataclass
class Title:
    """Earnable title."""
    id: str
    name: str
    prefix: bool  # True = prefix, False = suffix
    requirement: str
    color: str
    unlocked_at: Optional[str] = None


@dataclass
class AchievementStats:
    """Student achievement statistics."""
    total_points: int
    badges_unlocked: int
    total_badges: int
    titles_unlocked: int
    current_streak: int
    longest_streak: int
    completion_percentage: float
    rank: str
    next_milestone: Optional[str] = None


class AdvancedAchievementSystem:
    """
    Comprehensive achievement system for learning.
    
    Features:
    - Multi-tier badges
    - Earnable titles
    - Progress tracking
    - Category-based collections
    - Leaderboard integration
    """
    
    # Badge definitions
    BADGE_DEFINITIONS = [
        # Learning badges
        Badge("first_steps", "First Steps", "Complete your first lesson", "🌱", AchievementTier.BRONZE, AchievementCategory.LEARNING, 10, {"lessons_completed": 1}),
        Badge("quick_learner", "Quick Learner", "Complete 10 lessons in one day", "⚡", AchievementTier.SILVER, AchievementCategory.LEARNING, 50, {"daily_lessons": 10}),
        Badge("knowledge_seeker", "Knowledge Seeker", "Complete 50 lessons", "📚", AchievementTier.GOLD, AchievementCategory.LEARNING, 100, {"total_lessons": 50}),
        Badge("master_student", "Master Student", "Complete all lessons in a domain", "🎓", AchievementTier.PLATINUM, AchievementCategory.LEARNING, 250, {"domain_complete": True}),
        
        # Practice badges
        Badge("coder_novice", "Coder Novice", "Write your first 100 lines of code", "⌨️", AchievementTier.BRONZE, AchievementCategory.PRACTICE, 20, {"lines_of_code": 100}),
        Badge("debug_master", "Debug Master", "Fix 10 bugs in your code", "🐛", AchievementTier.SILVER, AchievementCategory.PRACTICE, 40, {"bugs_fixed": 10}),
        Badge("code_artisan", "Code Artisan", "Write 1000 lines of code", "✨", AchievementTier.GOLD, AchievementCategory.PRACTICE, 100, {"lines_of_code": 1000}),
        Badge("efficiency_expert", "Efficiency Expert", "Solve 5 problems with optimal solutions", "🚀", AchievementTier.PLATINUM, AchievementCategory.PRACTICE, 200, {"optimal_solutions": 5}),
        
        # Mastery badges
        Badge("quiz_whiz", "Quiz Whiz", "Score 100% on 5 quizzes", "🎯", AchievementTier.SILVER, AchievementCategory.MASTERY, 50, {"perfect_quizzes": 5}),
        Badge("concept_master", "Concept Master", "Master 20 concepts", "🧠", AchievementTier.GOLD, AchievementCategory.MASTERY, 150, {"concepts_mastered": 20}),
        Badge("speed_demon", "Speed Demon", "Solve a problem in under 1 minute", "⏱️", AchievementTier.SILVER, AchievementCategory.MASTERY, 30, {"fast_solve": True}),
        Badge("flawless", "Flawless", "Complete 10 challenges without errors", "💎", AchievementTier.PLATINUM, AchievementCategory.MASTERY, 200, {"perfect_challenges": 10}),
        
        # Social badges
        Badge("helpful_peer", "Helpful Peer", "Help another student once", "🤝", AchievementTier.BRONZE, AchievementCategory.SOCIAL, 15, {"help_given": 1}),
        Badge("community_star", "Community Star", "Help 10 students", "⭐", AchievementTier.SILVER, AchievementCategory.SOCIAL, 75, {"help_given": 10}),
        Badge("mentor", "Mentor", "Have 5 students thank you for help", "👨‍🏫", AchievementTier.GOLD, AchievementCategory.SOCIAL, 150, {"thanks_received": 5}),
        Badge("collaborator", "Collaborator", "Participate in 5 group sessions", "👥", AchievementTier.SILVER, AchievementCategory.SOCIAL, 50, {"group_sessions": 5}),
        
        # Challenge badges
        Badge("daily_warrior", "Daily Warrior", "Complete 7-day streak", "🔥", AchievementTier.SILVER, AchievementCategory.CHALLENGE, 70, {"streak_7": True}),
        Badge("monthly_master", "Monthly Master", "Complete 30-day streak", "📅", AchievementTier.GOLD, AchievementCategory.CHALLENGE, 300, {"streak_30": True}),
        Badge("night_owl", "Night Owl", "Study after midnight", "🦉", AchievementTier.BRONZE, AchievementCategory.CHALLENGE, 15, {"night_study": True}),
        Badge("early_bird", "Early Bird", "Study before 6 AM", "🐦", AchievementTier.BRONZE, AchievementCategory.CHALLENGE, 15, {"early_study": True}),
        Badge("weekend_warrior", "Weekend Warrior", "Study 4 hours on a weekend", "🎮", AchievementTier.SILVER, AchievementCategory.CHALLENGE, 40, {"weekend_hours": 4}),
        
        # Special badges
        Badge("beta_tester", "Beta Tester", "Participated in beta testing", "🧪", AchievementTier.PLATINUM, AchievementCategory.SPECIAL, 100, {"beta": True}),
        Badge("bug_hunter", "Bug Hunter", "Report a valid bug", "🔍", AchievementTier.GOLD, AchievementCategory.SPECIAL, 75, {"bug_reported": True}),
        Badge("founder", "Founder", "One of the first 100 students", "🏆", AchievementTier.DIAMOND, AchievementCategory.SPECIAL, 500, {"founder": True}),
        Badge("legend", "Legend", "Reach 5000 total points", "👑", AchievementTier.LEGENDARY, AchievementCategory.SPECIAL, 1000, {"total_points": 5000}),
    ]
    
    # Title definitions
    TITLE_DEFINITIONS = [
        Title("novice", "Novice", True, "Starting rank", "#8B4513", None),
        Title("beginner", "Beginner", True, "Complete 5 lessons", "#228B22", None),
        Title("student", "Student", True, "Complete 20 lessons", "#4169E1", None),
        Title("scholar", "Scholar", True, "Complete 50 lessons", "#9932CC", None),
        Title("expert", "Expert", True, "Master 30 concepts", "#FF6347", None),
        Title("master", "Master", True, "Complete all domains", "#FFD700", None),
        Title("grandmaster", "Grandmaster", True, "Reach 3000 points", "#FF1493", None),
        Title("legendary", "Legendary", True, "Reach 5000 points", "#00CED1", None),
        Title("the_coder", "the Coder", False, "Write 5000 lines", "#32CD32", None),
        Title("the_teacher", "the Teacher", False, "Help 50 students", "#FF8C00", None),
        Title("the_perfect", "the Perfect", False, "50 perfect scores", "#DC143C", None),
        Title("the_legend", "the Legend", False, "Unlock all badges", "#9400D3", None),
    ]
    
    def __init__(self):
        self.student_achievements: Dict[int, Dict] = {}
    
    def get_student_badges(self, student_id: int, progress_data: Dict) -> List[Badge]:
        """Get all badges with unlock status for student."""
        badges = []
        
        for badge_def in self.BADGE_DEFINITIONS:
            # Create copy
            badge = Badge(
                id=badge_def.id,
                name=badge_def.name,
                description=badge_def.description,
                icon=badge_def.icon,
                tier=badge_def.tier,
                category=badge_def.category,
                points=badge_def.points,
                criteria=badge_def.criteria,
            )
            
            # Check if unlocked
            is_unlocked, progress = self._check_badge_criteria(
                badge, progress_data
            )
            
            badge.progress = progress
            
            if is_unlocked:
                badge.unlocked_at = datetime.utcnow().isoformat()
            
            badges.append(badge)
        
        return badges
    
    def _check_badge_criteria(self, badge: Badge, progress: Dict) -> tuple:
        """Check if badge criteria are met."""
        criteria = badge.criteria
        
        # Check each criterion
        for key, value in criteria.items():
            if key == "lessons_completed":
                if progress.get("lessons_completed", 0) < value:
                    return False, progress.get("lessons_completed", 0) / value
            
            elif key == "daily_lessons":
                if progress.get("daily_lessons", 0) < value:
                    return False, progress.get("daily_lessons", 0) / value
            
            elif key == "total_lessons":
                if progress.get("total_lessons", 0) < value:
                    return False, progress.get("total_lessons", 0) / value
            
            elif key == "domain_complete":
                if not progress.get("domains_completed", []):
                    return False, 0.0
            
            elif key == "lines_of_code":
                current = progress.get("lines_of_code", 0)
                if current < value:
                    return False, current / value
            
            elif key == "bugs_fixed":
                current = progress.get("bugs_fixed", 0)
                if current < value:
                    return False, current / value
            
            elif key == "optimal_solutions":
                current = progress.get("optimal_solutions", 0)
                if current < value:
                    return False, current / value
            
            elif key == "perfect_quizzes":
                current = progress.get("perfect_quizzes", 0)
                if current < value:
                    return False, current / value
            
            elif key == "concepts_mastered":
                current = progress.get("concepts_mastered", 0)
                if current < value:
                    return False, current / value
            
            elif key == "fast_solve":
                if not progress.get("fast_solves", []):
                    return False, 0.0
            
            elif key == "perfect_challenges":
                current = progress.get("perfect_challenges", 0)
                if current < value:
                    return False, current / value
            
            elif key == "help_given":
                current = progress.get("help_given", 0)
                if current < value:
                    return False, current / value
            
            elif key == "thanks_received":
                current = progress.get("thanks_received", 0)
                if current < value:
                    return False, current / value
            
            elif key == "group_sessions":
                current = progress.get("group_sessions", 0)
                if current < value:
                    return False, current / value
            
            elif key == "streak_7":
                if progress.get("current_streak", 0) < 7:
                    return False, progress.get("current_streak", 0) / 7
            
            elif key == "streak_30":
                if progress.get("current_streak", 0) < 30:
                    return False, progress.get("current_streak", 0) / 30
            
            elif key in ["night_study", "early_study"]:
                if not progress.get(key, False):
                    return False, 1.0 if progress.get("study_times", []) else 0.0
            
            elif key == "weekend_hours":
                current = progress.get("weekend_hours", 0)
                if current < value:
                    return False, current / value
            
            elif key == "total_points":
                current = progress.get("total_points", 0)
                if current < value:
                    return False, current / value
        
        return True, 1.0
    
    def get_student_titles(self, student_id: int, progress_data: Dict) -> List[Title]:
        """Get all titles with unlock status."""
        titles = []
        
        for title_def in self.TITLE_DEFINITIONS:
            title = Title(
                id=title_def.id,
                name=title_def.name,
                prefix=title_def.prefix,
                requirement=title_def.requirement,
                color=title_def.color,
            )
            
            # Check unlock conditions
            is_unlocked = self._check_title_unlock(title, progress_data)
            if is_unlocked:
                title.unlocked_at = datetime.utcnow().isoformat()
            
            titles.append(title)
        
        return titles
    
    def _check_title_unlock(self, title: Title, progress: Dict) -> bool:
        """Check if title should be unlocked."""
        # Check based on requirements
        if title.id == "novice":
            return True
        
        elif title.id == "beginner":
            return progress.get("lessons_completed", 0) >= 5
        
        elif title.id == "student":
            return progress.get("lessons_completed", 0) >= 20
        
        elif title.id == "scholar":
            return progress.get("lessons_completed", 0) >= 50
        
        elif title.id == "expert":
            return progress.get("concepts_mastered", 0) >= 30
        
        elif title.id == "master":
            return len(progress.get("domains_completed", [])) >= 1
        
        elif title.id == "grandmaster":
            return progress.get("total_points", 0) >= 3000
        
        elif title.id == "legendary":
            return progress.get("total_points", 0) >= 5000
        
        elif title.id == "the_coder":
            return progress.get("lines_of_code", 0) >= 5000
        
        elif title.id == "the_teacher":
            return progress.get("help_given", 0) >= 50
        
        elif title.id == "the_perfect":
            return progress.get("perfect_quizzes", 0) >= 50
        
        elif title.id == "the_legend":
            # Check if all badges unlocked
            badges = self.get_student_badges(0, progress)
            return all(b.unlocked_at for b in badges)
        
        return False
    
    def calculate_stats(self, student_id: int, progress_data: Dict) -> AchievementStats:
        """Calculate student achievement statistics."""
        badges = self.get_student_badges(student_id, progress_data)
        titles = self.get_student_titles(student_id, progress_data)
        
        unlocked_badges = [b for b in badges if b.unlocked_at]
        unlocked_titles = [t for t in titles if t.unlocked_at]
        
        total_points = sum(b.points for b in unlocked_badges)
        
        # Determine rank
        rank = self._calculate_rank(total_points)
        
        # Calculate completion
        completion = len(unlocked_badges) / len(badges)
        
        # Find next milestone
        next_milestone = self._find_next_milestone(badges, progress_data)
        
        return AchievementStats(
            total_points=total_points,
            badges_unlocked=len(unlocked_badges),
            total_badges=len(badges),
            titles_unlocked=len(unlocked_titles),
            current_streak=progress_data.get("current_streak", 0),
            longest_streak=progress_data.get("longest_streak", 0),
            completion_percentage=round(completion * 100, 1),
            rank=rank,
            next_milestone=next_milestone,
        )
    
    def _calculate_rank(self, points: int) -> str:
        """Calculate rank based on points."""
        if points >= 5000:
            return "Legendary"
        elif points >= 3000:
            return "Grandmaster"
        elif points >= 1500:
            return "Master"
        elif points >= 750:
            return "Expert"
        elif points >= 300:
            return "Scholar"
        elif points >= 100:
            return "Student"
        else:
            return "Novice"
    
    def _find_next_milestone(self, badges: List[Badge], progress: Dict) -> Optional[str]:
        """Find the next achievable milestone."""
        locked_badges = [b for b in badges if not b.unlocked_at]
        
        if not locked_badges:
            return None
        
        # Find badge closest to unlocking
        closest = min(locked_badges, key=lambda b: 1 - b.progress)
        
        if closest.progress >= 0.8:
            return f"Almost there: {closest.name} ({closest.progress:.0%})"
        elif closest.progress >= 0.5:
            return f"Getting close: {closest.name} ({closest.progress:.0%})"
        else:
            return f"Next up: {closest.name}"
    
    def get_leaderboard_data(
        self,
        student_progress: Dict[int, Dict],
        limit: int = 10,
    ) -> List[Dict]:
        """Generate leaderboard data."""
        leaderboard = []
        
        for student_id, progress in student_progress.items():
            stats = self.calculate_stats(student_id, progress)
            
            # Get active title
            titles = self.get_student_titles(student_id, progress)
            active_title = next(
                (t for t in reversed(titles) if t.unlocked_at),
                None
            )
            
            leaderboard.append({
                "student_id": student_id,
                "name": progress.get("name", f"Student {student_id}"),
                "total_points": stats.total_points,
                "badges": stats.badges_unlocked,
                "rank": stats.rank,
                "title": active_title.name if active_title else "Novice",
                "title_color": active_title.color if active_title else "#8B4513",
            })
        
        # Sort by points
        leaderboard.sort(key=lambda x: x["total_points"], reverse=True)
        
        return leaderboard[:limit]
    
    def get_category_progress(
        self,
        student_id: int,
        progress_data: Dict,
    ) -> Dict[AchievementCategory, Dict]:
        """Get progress by achievement category."""
        badges = self.get_student_badges(student_id, progress_data)
        
        category_progress = {}
        
        for category in AchievementCategory:
            category_badges = [b for b in badges if b.category == category]
            unlocked = [b for b in category_badges if b.unlocked_at]
            
            category_progress[category] = {
                "total": len(category_badges),
                "unlocked": len(unlocked),
                "points": sum(b.points for b in unlocked),
                "completion": len(unlocked) / len(category_badges) if category_badges else 0,
            }
        
        return category_progress


def get_student_achievements(student_id: int, progress_data: Dict) -> Dict:
    """
    Main API-facing function for achievement data.
    
    Args:
        student_id: Student ID
        progress_data: Student progress data
    
    Returns:
        Complete achievement information
    """
    system = AdvancedAchievementSystem()
    
    badges = system.get_student_badges(student_id, progress_data)
    titles = system.get_student_titles(student_id, progress_data)
    stats = system.calculate_stats(student_id, progress_data)
    categories = system.get_category_progress(student_id, progress_data)
    
    return {
        "stats": {
            "total_points": stats.total_points,
            "badges_unlocked": stats.badges_unlocked,
            "total_badges": stats.total_badges,
            "titles_unlocked": stats.titles_unlocked,
            "completion_percentage": stats.completion_percentage,
            "current_streak": stats.current_streak,
            "longest_streak": stats.longest_streak,
            "rank": stats.rank,
            "next_milestone": stats.next_milestone,
        },
        "badges": [
            {
                "id": b.id,
                "name": b.name,
                "description": b.description,
                "icon": b.icon,
                "tier": b.tier.value,
                "category": b.category.value,
                "points": b.points,
                "unlocked": b.unlocked_at is not None,
                "unlocked_at": b.unlocked_at,
                "progress": round(b.progress * 100, 1),
            }
            for b in badges
        ],
        "titles": [
            {
                "id": t.id,
                "name": t.name,
                "prefix": t.prefix,
                "requirement": t.requirement,
                "color": t.color,
                "unlocked": t.unlocked_at is not None,
                "unlocked_at": t.unlocked_at,
            }
            for t in titles
        ],
        "categories": {
            k.value: {
                "total": v["total"],
                "unlocked": v["unlocked"],
                "points": v["points"],
                "completion": round(v["completion"] * 100, 1),
            }
            for k, v in categories.items()
        },
    }
