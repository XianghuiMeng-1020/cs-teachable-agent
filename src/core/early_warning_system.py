"""
Early Warning System for Learning Difficulties

Predicts and alerts when students are at risk of falling behind.
Uses machine learning patterns and educational research indicators.

Research Applications:
- At-risk student identification
- Intervention timing optimization
- Learning pattern analysis
- Dropout prediction
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
import math


class RiskLevel(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskIndicator:
    """A specific risk indicator."""
    indicator_type: str
    severity: RiskLevel
    value: float
    threshold: float
    description: str
    recommendation: str
    trend: str  # "improving", "stable", "declining"


@dataclass
class StudentRiskProfile:
    """Complete risk profile for a student."""
    user_id: int
    overall_risk: RiskLevel
    risk_score: float  # 0-100
    indicators: List[RiskIndicator]
    last_activity_date: Optional[str]
    days_since_active: int
    trend_direction: str
    intervention_urgency: str
    predicted_outcome: str
    generated_at: str


class EarlyWarningSystem:
    """
    Early Warning System for identifying at-risk students.
    
    Uses multiple indicators:
    - Engagement decline
    - Performance drops
    - Inactivity patterns
    - Conceptual struggle indicators
    - Help-seeking behavior
    """
    
    # Risk thresholds
    RISK_THRESHOLDS = {
        "engagement_decline": 0.7,  # 30% drop
        "low_activity": 3,  # 3 days inactive
        "high_inactivity": 7,  # 1 week inactive
        "struggling_rate": 0.6,  # 60% struggling
        "low_quality_ratio": 0.5,  # 50% low quality submissions
    }
    
    def __init__(self):
        self.indicators_weights = {
            "inactivity": 0.25,
            "engagement_decline": 0.20,
            "performance_drop": 0.20,
            "struggling_concepts": 0.20,
            "help_seeking": 0.15,
        }
    
    def analyze_student(
        self,
        user_id: int,
        activity_history: List[Dict],
        learning_events: List[Dict],
        test_results: List[Dict],
        current_streak: int = 0,
        gamification_data: Optional[Dict] = None,
    ) -> StudentRiskProfile:
        """
        Analyze student and generate risk profile.
        
        Args:
            user_id: Student ID
            activity_history: List of activity records
            learning_events: Teaching and test events
            test_results: Test attempt results
            current_streak: Current learning streak
            gamification_data: Gamification stats
        
        Returns:
            Complete risk profile
        """
        indicators = []
        
        # 1. Inactivity Analysis
        inactivity_indicator = self._analyze_inactivity(activity_history)
        if inactivity_indicator:
            indicators.append(inactivity_indicator)
        
        # 2. Engagement Trend
        engagement_indicator = self._analyze_engagement_trend(learning_events)
        if engagement_indicator:
            indicators.append(engagement_indicator)
        
        # 3. Performance Analysis
        performance_indicator = self._analyze_performance(test_results)
        if performance_indicator:
            indicators.append(performance_indicator)
        
        # 4. Struggling Concepts
        struggle_indicator = self._analyze_struggling_concepts(learning_events)
        if struggle_indicator:
            indicators.append(struggle_indicator)
        
        # 5. Help Seeking Behavior
        help_indicator = self._analyze_help_seeking(learning_events)
        if help_indicator:
            indicators.append(help_indicator)
        
        # Calculate overall risk
        risk_score = self._calculate_risk_score(indicators)
        overall_risk = self._score_to_risk_level(risk_score)
        
        # Determine trend
        trend = self._determine_trend(indicators)
        
        # Get last activity
        last_activity = self._get_last_activity_date(activity_history)
        days_inactive = self._days_since(last_activity) if last_activity else 999
        
        # Determine urgency and outcome
        urgency = self._determine_urgency(overall_risk, days_inactive, current_streak)
        predicted_outcome = self._predict_outcome(risk_score, trend, current_streak)
        
        return StudentRiskProfile(
            user_id=user_id,
            overall_risk=overall_risk,
            risk_score=round(risk_score, 1),
            indicators=indicators,
            last_activity_date=last_activity.isoformat() if last_activity else None,
            days_since_active=days_inactive,
            trend_direction=trend,
            intervention_urgency=urgency,
            predicted_outcome=predicted_outcome,
            generated_at=datetime.utcnow().isoformat(),
        )
    
    def _analyze_inactivity(self, activity_history: List[Dict]) -> Optional[RiskIndicator]:
        """Analyze inactivity patterns."""
        if not activity_history:
            return RiskIndicator(
                indicator_type="inactivity",
                severity=RiskLevel.CRITICAL,
                value=999,
                threshold=7,
                description="No recorded activity",
                recommendation="Immediate intervention required - student has not engaged with system",
                trend="declining",
            )
        
        # Get recent activity
        recent = [a for a in activity_history if self._is_recent(a.get("timestamp"), days=7)]
        
        if not recent:
            # No activity in last week
            last_date = self._get_last_activity_date(activity_history)
            days = self._days_since(last_date) if last_date else 7
            
            return RiskIndicator(
                indicator_type="inactivity",
                severity=RiskLevel.HIGH if days > 7 else RiskLevel.MEDIUM,
                value=days,
                threshold=self.RISK_THRESHOLDS["high_inactivity"],
                description=f"No activity for {days} days",
                recommendation="Send re-engagement email and check for technical issues",
                trend="declining",
            )
        
        return None
    
    def _analyze_engagement_trend(self, learning_events: List[Dict]) -> Optional[RiskIndicator]:
        """Analyze engagement trend over time."""
        if len(learning_events) < 5:
            return None
        
        # Split into first and second half
        mid = len(learning_events) // 2
        first_half = learning_events[:mid]
        second_half = learning_events[mid:]
        
        # Calculate activity counts
        first_activity = sum(1 for e in first_half if e.get("type") == "teach")
        second_activity = sum(1 for e in second_half if e.get("type") == "teach")
        
        if first_activity == 0:
            return None
        
        decline_ratio = second_activity / first_activity
        
        if decline_ratio < self.RISK_THRESHOLDS["engagement_decline"]:
            return RiskIndicator(
                indicator_type="engagement_decline",
                severity=RiskLevel.MEDIUM if decline_ratio > 0.5 else RiskLevel.HIGH,
                value=round(decline_ratio * 100, 1),
                threshold=70,
                description=f"Engagement dropped by {round((1 - decline_ratio) * 100)}%",
                recommendation="Consider varying content or adjusting difficulty",
                trend="declining",
            )
        
        return None
    
    def _analyze_performance(self, test_results: List[Dict]) -> Optional[RiskIndicator]:
        """Analyze test performance trends."""
        if len(test_results) < 3:
            return None
        
        # Calculate pass rate
        passed = sum(1 for t in test_results if t.get("passed", False))
        total = len(test_results)
        pass_rate = passed / total
        
        # Check recent trend
        recent = test_results[-3:]
        recent_passed = sum(1 for t in recent if t.get("passed", False))
        recent_rate = recent_passed / len(recent)
        
        if pass_rate < 0.5:
            return RiskIndicator(
                indicator_type="performance_drop",
                severity=RiskLevel.HIGH,
                value=round(pass_rate * 100, 1),
                threshold=50,
                description=f"Low overall pass rate: {round(pass_rate * 100)}%",
                recommendation="Review fundamental concepts and provide additional practice",
                trend="stable" if abs(pass_rate - recent_rate) < 0.1 else "declining",
            )
        
        if recent_rate < pass_rate - 0.2:
            return RiskIndicator(
                indicator_type="performance_drop",
                severity=RiskLevel.MEDIUM,
                value=round(recent_rate * 100, 1),
                threshold=round(pass_rate * 100, 1),
                description="Recent performance below average",
                recommendation="Identify specific struggling areas and provide targeted help",
                trend="declining",
            )
        
        return None
    
    def _analyze_struggling_concepts(self, learning_events: List[Dict]) -> Optional[RiskIndicator]:
        """Analyze struggling with concepts."""
        if not learning_events:
            return None
        
        # Count repeated teaching on same concepts
        concept_attempts: Dict[str, int] = {}
        for event in learning_events:
            concept = event.get("concept", "")
            if concept:
                concept_attempts[concept] = concept_attempts.get(concept, 0) + 1
        
        # Find concepts with >2 attempts (struggling)
        struggling = [c for c, count in concept_attempts.items() if count > 2]
        
        if len(struggling) > len(concept_attempts) * 0.3:
            return RiskIndicator(
                indicator_type="struggling_concepts",
                severity=RiskLevel.MEDIUM,
                value=len(struggling),
                threshold=len(concept_attempts) * 0.3,
                description=f"Struggling with {len(struggling)} concepts",
                recommendation="Provide alternative explanations and more examples",
                trend="stable",
            )
        
        return None
    
    def _analyze_help_seeking(self, learning_events: List[Dict]) -> Optional[RiskIndicator]:
        """Analyze help-seeking behavior."""
        if not learning_events:
            return None
        
        # Look for help-seeking patterns
        help_events = [e for e in learning_events if e.get("help_requested", False)]
        
        if len(help_events) > len(learning_events) * 0.5:
            return RiskIndicator(
                indicator_type="help_seeking",
                severity=RiskLevel.LOW,
                value=len(help_events),
                threshold=len(learning_events) * 0.3,
                description=f"Frequent help requests: {len(help_events)} times",
                recommendation="Student is engaged but may need more scaffolding",
                trend="stable",
            )
        
        return None
    
    def _calculate_risk_score(self, indicators: List[RiskIndicator]) -> float:
        """Calculate overall risk score from indicators."""
        if not indicators:
            return 0.0
        
        total_weight = 0
        weighted_sum = 0
        
        severity_weights = {
            RiskLevel.LOW: 25,
            RiskLevel.MEDIUM: 50,
            RiskLevel.HIGH: 75,
            RiskLevel.CRITICAL: 100,
        }
        
        for indicator in indicators:
            weight = self.indicators_weights.get(indicator.indicator_type, 0.15)
            score = severity_weights.get(indicator.severity, 50)
            
            weighted_sum += score * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0
    
    def _score_to_risk_level(self, score: float) -> RiskLevel:
        """Convert numeric score to risk level."""
        if score >= 75:
            return RiskLevel.CRITICAL
        if score >= 60:
            return RiskLevel.HIGH
        if score >= 40:
            return RiskLevel.MEDIUM
        if score >= 20:
            return RiskLevel.LOW
        return RiskLevel.NONE
    
    def _determine_trend(self, indicators: List[RiskIndicator]) -> str:
        """Determine overall trend from indicators."""
        if not indicators:
            return "stable"
        
        trends = [i.trend for i in indicators]
        
        if trends.count("declining") > len(trends) * 0.5:
            return "declining"
        if trends.count("improving") > len(trends) * 0.5:
            return "improving"
        return "stable"
    
    def _determine_urgency(
        self,
        risk: RiskLevel,
        days_inactive: int,
        streak: int
    ) -> str:
        """Determine intervention urgency."""
        if risk == RiskLevel.CRITICAL:
            return "immediate"
        if risk == RiskLevel.HIGH or days_inactive > 7:
            return "within_24h"
        if risk == RiskLevel.MEDIUM or streak == 0:
            return "within_week"
        return "monitor"
    
    def _predict_outcome(self, risk_score: float, trend: str, streak: int) -> str:
        """Predict learning outcome based on current trajectory."""
        if risk_score > 75:
            return "at_risk_dropout"
        if risk_score > 50 or trend == "declining":
            return "may_fall_behind"
        if risk_score < 25 and streak > 5:
            return "on_track_excellent"
        return "on_track"
    
    def _get_last_activity_date(self, activity_history: List[Dict]) -> Optional[datetime]:
        """Get last activity date from history."""
        if not activity_history:
            return None
        
        dates = []
        for activity in activity_history:
            ts = activity.get("timestamp")
            if ts:
                try:
                    dates.append(datetime.fromisoformat(ts.replace("Z", "+00:00")))
                except:
                    pass
        
        return max(dates) if dates else None
    
    def _days_since(self, date: datetime) -> int:
        """Calculate days since given date."""
        return (datetime.utcnow() - date).days
    
    def _is_recent(self, timestamp: str, days: int = 7) -> bool:
        """Check if timestamp is within recent days."""
        if not timestamp:
            return False
        try:
            date = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            return (datetime.utcnow() - date).days <= days
        except:
            return False
    
    def get_class_risk_summary(
        self,
        student_profiles: List[StudentRiskProfile]
    ) -> Dict[str, any]:
        """Get summary statistics for a class/group."""
        if not student_profiles:
            return {"message": "No student data"}
        
        risk_counts = {
            RiskLevel.NONE: 0,
            RiskLevel.LOW: 0,
            RiskLevel.MEDIUM: 0,
            RiskLevel.HIGH: 0,
            RiskLevel.CRITICAL: 0,
        }
        
        for profile in student_profiles:
            risk_counts[profile.overall_risk] += 1
        
        total = len(student_profiles)
        
        return {
            "total_students": total,
            "risk_distribution": {
                k.value: v for k, v in risk_counts.items()
            },
            "at_risk_percentage": round(
                (risk_counts[RiskLevel.HIGH] + risk_counts[RiskLevel.CRITICAL]) / total * 100,
                1
            ),
            "average_risk_score": round(
                sum(p.risk_score for p in student_profiles) / total,
                1
            ),
            "students_needing_intervention": [
                {
                    "user_id": p.user_id,
                    "risk_level": p.overall_risk.value,
                    "urgency": p.intervention_urgency,
                }
                for p in student_profiles
                if p.overall_risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]
            ],
        }


def analyze_student_risk(
    user_id: int,
    activity_history: List[Dict],
    learning_events: List[Dict],
    test_results: List[Dict],
    current_streak: int = 0,
) -> StudentRiskProfile:
    """
    Main API-facing function for risk analysis.
    
    This is the convenience function that wraps the EarlyWarningSystem.
    """
    ews = EarlyWarningSystem()
    return ews.analyze_student(
        user_id=user_id,
        activity_history=activity_history,
        learning_events=learning_events,
        test_results=test_results,
        current_streak=current_streak,
    )
