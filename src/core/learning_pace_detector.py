"""
Adaptive Learning Pace Detection System

Dynamically detects and adapts to individual student learning speeds.
Uses real-time performance metrics to optimize teaching rhythm.

Research Applications:
- Personalized pacing in education
- Cognitive load management
- Learning efficiency optimization
- Adaptive instruction timing
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
import statistics


class PaceCategory(Enum):
    """Learning pace categories."""
    VERY_SLOW = "very_slow"      # Needs extra time
    SLOW = "slow"                # Slightly below average
    AVERAGE = "average"          # Normal pace
    FAST = "fast"                # Above average
    VERY_FAST = "very_fast"      # Accelerated


class EngagementLevel(Enum):
    """Student engagement levels."""
    DISENGAGED = "disengaged"
    PASSIVE = "passive"
    MODERATE = "moderate"
    ACTIVE = "active"
    HIGHLY_ACTIVE = "highly_active"


@dataclass
class PaceMetrics:
    """Metrics for learning pace analysis."""
    time_per_concept: float  # minutes
    response_time_avg: float  # seconds
    help_requests_per_session: float
    revision_frequency: float  # how often they review
    pause_patterns: List[float]  # pause durations
    peak_performance_hours: List[int]
    

@dataclass
class PaceProfile:
    """Complete pace profile for a student."""
    student_id: int
    pace_category: PaceCategory
    engagement_level: EngagementLevel
    metrics: PaceMetrics
    recommended_speed_multiplier: float  # 0.5 to 2.0
    optimal_session_length: int  # minutes
    recommended_break_interval: int  # minutes
    best_learning_times: List[str]  # ["morning", "afternoon", "evening"]
    adaptation_history: List[Dict] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class LearningPaceDetector:
    """
    Detects and analyzes individual learning pace.
    
    Key features:
    - Real-time pace tracking
    - Engagement correlation
    - Optimal timing recommendations
    - Fatigue detection
    """
    
    # Reference values for pace categorization
    PACE_THRESHOLDS = {
        "time_per_concept": {
            PaceCategory.VERY_FAST: 3,    # < 3 min
            PaceCategory.FAST: 5,         # 3-5 min
            PaceCategory.AVERAGE: 10,     # 5-10 min
            PaceCategory.SLOW: 15,        # 10-15 min
            PaceCategory.VERY_SLOW: 999,  # > 15 min
        },
        "response_time": {
            PaceCategory.VERY_FAST: 10,   # < 10 sec
            PaceCategory.FAST: 20,      # 10-20 sec
            PaceCategory.AVERAGE: 45,   # 20-45 sec
            PaceCategory.SLOW: 90,      # 45-90 sec
            PaceCategory.VERY_SLOW: 999, # > 90 sec
        },
    }
    
    def __init__(self):
        self.min_session_data = 3  # Minimum sessions for reliable detection
    
    def analyze_learning_sessions(
        self,
        student_id: int,
        session_data: List[Dict],
    ) -> PaceProfile:
        """
        Analyze learning sessions to detect pace.
        
        Args:
            student_id: Student ID
            session_data: List of session records
        
        Returns:
            PaceProfile with recommendations
        """
        if len(session_data) < self.min_session_data:
            # Return default profile for new students
            return self._create_default_profile(student_id)
        
        # Calculate metrics
        metrics = self._calculate_metrics(session_data)
        
        # Determine pace category
        pace_category = self._categorize_pace(metrics)
        
        # Determine engagement level
        engagement = self._assess_engagement(session_data, metrics)
        
        # Generate recommendations
        speed_multiplier = self._calculate_speed_multiplier(
            pace_category, engagement, metrics
        )
        
        optimal_session = self._calculate_optimal_session_length(
            metrics, engagement
        )
        
        break_interval = self._calculate_break_interval(metrics)
        
        best_times = self._identify_peak_times(session_data)
        
        return PaceProfile(
            student_id=student_id,
            pace_category=pace_category,
            engagement_level=engagement,
            metrics=metrics,
            recommended_speed_multiplier=round(speed_multiplier, 2),
            optimal_session_length=optimal_session,
            recommended_break_interval=break_interval,
            best_learning_times=best_times,
            adaptation_history=[],
        )
    
    def _calculate_metrics(self, sessions: List[Dict]) -> PaceMetrics:
        """Calculate learning pace metrics."""
        # Time per concept
        concept_times = []
        for session in sessions:
            duration = session.get("duration_minutes", 0)
            concepts = session.get("concepts_learned", 1)
            if concepts > 0:
                concept_times.append(duration / concepts)
        
        avg_time_per_concept = statistics.mean(concept_times) if concept_times else 10.0
        
        # Response times
        response_times = []
        for session in sessions:
            if "response_times" in session:
                response_times.extend(session["response_times"])
        
        avg_response_time = statistics.mean(response_times) if response_times else 30.0
        
        # Help requests
        help_requests = [s.get("help_requests", 0) for s in sessions]
        avg_help_requests = statistics.mean(help_requests) if help_requests else 0
        
        # Revision frequency
        revisions = [s.get("revisions", 0) for s in sessions]
        avg_revisions = statistics.mean(revisions) if revisions else 0
        
        # Pause patterns
        pauses = []
        for session in sessions:
            if "pauses" in session:
                pauses.extend(session["pauses"])
        
        # Peak performance hours
        peak_hours = self._analyze_peak_hours(sessions)
        
        return PaceMetrics(
            time_per_concept=round(avg_time_per_concept, 1),
            response_time_avg=round(avg_response_time, 1),
            help_requests_per_session=round(avg_help_requests, 1),
            revision_frequency=round(avg_revisions, 1),
            pause_patterns=pauses[:10],  # Keep last 10
            peak_performance_hours=peak_hours,
        )
    
    def _categorize_pace(self, metrics: PaceMetrics) -> PaceCategory:
        """Categorize learning pace."""
        time_per_concept = metrics.time_per_concept
        
        thresholds = self.PACE_THRESHOLDS["time_per_concept"]
        
        if time_per_concept < thresholds[PaceCategory.VERY_FAST]:
            return PaceCategory.VERY_FAST
        elif time_per_concept < thresholds[PaceCategory.FAST]:
            return PaceCategory.FAST
        elif time_per_concept < thresholds[PaceCategory.AVERAGE]:
            return PaceCategory.AVERAGE
        elif time_per_concept < thresholds[PaceCategory.SLOW]:
            return PaceCategory.SLOW
        else:
            return PaceCategory.VERY_SLOW
    
    def _assess_engagement(
        self,
        sessions: List[Dict],
        metrics: PaceMetrics,
    ) -> EngagementLevel:
        """Assess student engagement level."""
        # Calculate engagement score
        recent_sessions = sessions[-5:] if len(sessions) > 5 else sessions
        
        # Factors
        session_frequency = len(recent_sessions)
        interaction_count = sum(s.get("interactions", 0) for s in recent_sessions)
        question_asked = sum(1 for s in recent_sessions if s.get("questions_asked", 0) > 0)
        
        # Engagement score (0-100)
        score = 0
        score += min(30, session_frequency * 6)  # Up to 30 points for frequency
        score += min(40, interaction_count * 2)   # Up to 40 points for interaction
        score += min(30, question_asked * 10)     # Up to 30 points for curiosity
        
        # Long pauses reduce engagement score
        long_pauses = sum(1 for p in metrics.pause_patterns if p > 300)  # > 5 min
        score -= long_pauses * 10
        
        # Categorize
        if score >= 80:
            return EngagementLevel.HIGHLY_ACTIVE
        elif score >= 60:
            return EngagementLevel.ACTIVE
        elif score >= 40:
            return EngagementLevel.MODERATE
        elif score >= 20:
            return EngagementLevel.PASSIVE
        else:
            return EngagementLevel.DISENGAGED
    
    def _calculate_speed_multiplier(
        self,
        pace: PaceCategory,
        engagement: EngagementLevel,
        metrics: PaceMetrics,
    ) -> float:
        """Calculate recommended speed multiplier."""
        base_multiplier = {
            PaceCategory.VERY_SLOW: 0.6,
            PaceCategory.SLOW: 0.8,
            PaceCategory.AVERAGE: 1.0,
            PaceCategory.FAST: 1.3,
            PaceCategory.VERY_FAST: 1.5,
        }.get(pace, 1.0)
        
        # Adjust based on engagement
        engagement_adjustment = {
            EngagementLevel.DISENGAGED: -0.3,
            EngagementLevel.PASSIVE: -0.1,
            EngagementLevel.MODERATE: 0.0,
            EngagementLevel.ACTIVE: 0.1,
            EngagementLevel.HIGHLY_ACTIVE: 0.2,
        }.get(engagement, 0.0)
        
        # Adjust based on help requests (struggling = slower)
        if metrics.help_requests_per_session > 3:
            engagement_adjustment -= 0.2
        
        final_multiplier = base_multiplier + engagement_adjustment
        return max(0.5, min(2.0, final_multiplier))
    
    def _calculate_optimal_session_length(
        self,
        metrics: PaceMetrics,
        engagement: EngagementLevel,
    ) -> int:
        """Calculate optimal session length in minutes."""
        # Base length
        base_length = 25  # Pomodoro standard
        
        # Adjust by pace
        if metrics.time_per_concept > 10:  # Slow learner
            base_length = 20  # Shorter sessions
        elif metrics.time_per_concept < 5:  # Fast learner
            base_length = 30  # Can handle longer
        
        # Adjust by engagement
        engagement_factor = {
            EngagementLevel.DISENGAGED: 0.7,
            EngagementLevel.PASSIVE: 0.8,
            EngagementLevel.MODERATE: 1.0,
            EngagementLevel.ACTIVE: 1.2,
            EngagementLevel.HIGHLY_ACTIVE: 1.3,
        }.get(engagement, 1.0)
        
        optimal = int(base_length * engagement_factor)
        return max(15, min(45, optimal))
    
    def _calculate_break_interval(self, metrics: PaceMetrics) -> int:
        """Calculate recommended break interval."""
        # Base interval
        interval = 25
        
        # Adjust based on fatigue indicators
        if metrics.pause_patterns:
            avg_pause = statistics.mean(metrics.pause_patterns)
            if avg_pause > 180:  # > 3 min average pause
                interval = 20  # Need more frequent breaks
        
        # Slow learners need more frequent breaks
        if metrics.time_per_concept > 10:
            interval = max(15, interval - 5)
        
        return interval
    
    def _identify_peak_times(self, sessions: List[Dict]) -> List[str]:
        """Identify best learning times of day."""
        hour_performance = {}
        
        for session in sessions:
            hour = session.get("hour_of_day", 12)
            performance = session.get("performance_score", 0.5)
            
            if hour not in hour_performance:
                hour_performance[hour] = []
            hour_performance[hour].append(performance)
        
        # Calculate average performance by hour
        hour_avg = {
            h: statistics.mean(scores) 
            for h, scores in hour_performance.items() 
            if len(scores) >= 2
        }
        
        # Map to time periods
        time_periods = {
            "morning": [6, 7, 8, 9, 10, 11],
            "afternoon": [12, 13, 14, 15, 16, 17],
            "evening": [18, 19, 20, 21, 22, 23],
        }
        
        period_scores = {}
        for period, hours in time_periods.items():
            scores = [hour_avg.get(h, 0) for h in hours if h in hour_avg]
            if scores:
                period_scores[period] = statistics.mean(scores)
        
        # Return sorted by performance
        sorted_periods = sorted(
            period_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [p[0] for p in sorted_periods[:2]] if sorted_periods else ["afternoon"]
    
    def _analyze_peak_hours(self, sessions: List[Dict]) -> List[int]:
        """Analyze which hours have best performance."""
        hour_scores = {}
        
        for session in sessions:
            hour = session.get("hour_of_day", 12)
            score = session.get("performance_score", 0.5)
            
            if hour not in hour_scores:
                hour_scores[hour] = []
            hour_scores[hour].append(score)
        
        # Calculate averages and find top 3
        hour_avg = {
            h: statistics.mean(scores) 
            for h, scores in hour_scores.items() 
            if len(scores) >= 2
        }
        
        sorted_hours = sorted(hour_avg.items(), key=lambda x: x[1], reverse=True)
        return [h[0] for h in sorted_hours[:3]]
    
    def _create_default_profile(self, student_id: int) -> PaceProfile:
        """Create default profile for new students."""
        return PaceProfile(
            student_id=student_id,
            pace_category=PaceCategory.AVERAGE,
            engagement_level=EngagementLevel.MODERATE,
            metrics=PaceMetrics(
                time_per_concept=8.0,
                response_time_avg=30.0,
                help_requests_per_session=1.0,
                revision_frequency=0.5,
                pause_patterns=[],
                peak_performance_hours=[14, 15, 16],
            ),
            recommended_speed_multiplier=1.0,
            optimal_session_length=25,
            recommended_break_interval=25,
            best_learning_times=["afternoon"],
        )
    
    def detect_fatigue(
        self,
        recent_sessions: List[Dict],
        window_size: int = 3,
    ) -> Dict[str, any]:
        """
        Detect signs of learning fatigue.
        
        Returns fatigue indicators and recommendations.
        """
        if len(recent_sessions) < window_size:
            return {"fatigue_detected": False, "confidence": 0}
        
        recent = recent_sessions[-window_size:]
        
        indicators = []
        
        # Check for declining performance
        performances = [s.get("performance_score", 0.5) for s in recent]
        if len(performances) >= 2:
            if performances[-1] < performances[0] * 0.8:
                indicators.append("performance_decline")
        
        # Check for increasing error rates
        error_rates = [s.get("error_rate", 0) for s in recent]
        if len(error_rates) >= 2:
            if error_rates[-1] > error_rates[0] * 1.5:
                indicators.append("error_increase")
        
        # Check for longer response times
        response_times = [s.get("avg_response_time", 30) for s in recent]
        if len(response_times) >= 2:
            if response_times[-1] > response_times[0] * 1.3:
                indicators.append("slower_responses")
        
        # Check for session duration dropping
        durations = [s.get("duration_minutes", 0) for s in recent]
        if durations and statistics.mean(durations) < 15:
            indicators.append("shorter_sessions")
        
        fatigue_detected = len(indicators) >= 2
        
        return {
            "fatigue_detected": fatigue_detected,
            "confidence": min(1.0, len(indicators) * 0.3),
            "indicators": indicators,
            "recommendations": [
                "Take a longer break (30+ minutes)" if fatigue_detected else "Continue as normal",
                "Switch to a different type of activity" if "performance_decline" in indicators else None,
                "Review previous concepts before continuing" if "error_increase" in indicators else None,
            ],
        }
    
    def get_pace_recommendations(self, profile: PaceProfile) -> List[str]:
        """Generate personalized pacing recommendations."""
        recommendations = []
        
        # Pace-based recommendations
        if profile.pace_category == PaceCategory.VERY_SLOW:
            recommendations.append("Allocate extra time for complex concepts")
            recommendations.append("Use scaffolded examples with step-by-step guidance")
        elif profile.pace_category == PaceCategory.SLOW:
            recommendations.append("Provide additional practice opportunities")
        elif profile.pace_category == PaceCategory.FAST:
            recommendations.append("Offer challenging extensions to concepts")
            recommendations.append("Consider accelerating through review material")
        elif profile.pace_category == PaceCategory.VERY_FAST:
            recommendations.append("Provide advanced challenges and enrichment activities")
            recommendations.append("Allow self-paced exploration of topics")
        
        # Engagement-based recommendations
        if profile.engagement_level == EngagementLevel.DISENGAGED:
            recommendations.append("Incorporate more interactive elements")
            recommendations.append("Check for external factors affecting engagement")
        elif profile.engagement_level == EngagementLevel.HIGHLY_ACTIVE:
            recommendations.append("Leverage high engagement with collaborative activities")
        
        # Timing recommendations
        if profile.best_learning_times:
            recommendations.append(
                f"Schedule challenging content during {profile.best_learning_times[0]} hours"
            )
        
        return recommendations


def detect_learning_pace(
    student_id: int,
    session_history: List[Dict],
) -> Dict[str, any]:
    """
    Main API-facing function for pace detection.
    
    Args:
        student_id: Student ID
        session_history: List of learning session records
    
    Returns:
        Pace profile as dictionary
    """
    detector = LearningPaceDetector()
    profile = detector.analyze_learning_sessions(student_id, session_history)
    
    # Convert to dict for API response
    return {
        "student_id": profile.student_id,
        "pace_category": profile.pace_category.value,
        "engagement_level": profile.engagement_level.value,
        "metrics": {
            "time_per_concept": profile.metrics.time_per_concept,
            "response_time_avg": profile.metrics.response_time_avg,
            "help_requests_per_session": profile.metrics.help_requests_per_session,
            "revision_frequency": profile.metrics.revision_frequency,
        },
        "recommendations": {
            "speed_multiplier": profile.recommended_speed_multiplier,
            "optimal_session_length": profile.optimal_session_length,
            "recommended_break_interval": profile.recommended_break_interval,
            "best_learning_times": profile.best_learning_times,
        },
        "personalized_tips": detector.get_pace_recommendations(profile),
        "generated_at": profile.generated_at,
    }
