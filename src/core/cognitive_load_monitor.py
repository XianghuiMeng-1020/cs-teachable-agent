"""
Cognitive Load Monitoring System

Real-time monitoring of student's cognitive load to prevent overload.
Uses behavioral indicators and performance metrics.

Research Applications:
- Cognitive load theory in education
- Optimal challenge point theory
- Working memory management
- Adaptive difficulty adjustment
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import statistics


class CognitiveLoadLevel(Enum):
    """Levels of cognitive load."""
    VERY_LOW = "very_low"      # Under-challenged
    LOW = "low"                # Comfortable
    OPTIMAL = "optimal"        # Sweet spot for learning
    HIGH = "high"              # Challenging but manageable
    OVERLOAD = "overload"      # Too difficult, reduce load


class LoadType(Enum):
    """Types of cognitive load (based on CLT)."""
    INTRINSIC = "intrinsic"      # Complexity of the material
    EXTRANEOUS = "extraneous"    # Unnecessary processing
    GERMANE = "germane"          # Beneficial processing


@dataclass
class LoadIndicators:
    """Behavioral and performance indicators."""
    error_rate: float
    response_time_increase: float  # % increase from baseline
    help_requests: int
    pause_frequency: float
    revision_count: int
    hesitation_count: int
    gaze_pattern_complexity: float  # if eye tracking available
    keystroke_dynamics: float  # typing rhythm changes


@dataclass
class CognitiveLoadAssessment:
    """Complete cognitive load assessment."""
    student_id: int
    current_load: CognitiveLoadLevel
    load_score: float  # 0-100
    indicators: LoadIndicators
    breakdown: Dict[LoadType, float]
    recommended_action: str
    difficulty_adjustment: float  # -0.3 to +0.3
    break_recommended: bool
    timestamp: str


class CognitiveLoadMonitor:
    """
    Monitors and manages cognitive load in real-time.
    
    Based on Cognitive Load Theory (Sweller):
    - Total CL = Intrinsic + Extraneous + Germane
    - Goal: Minimize extraneous, optimize germane
    """
    
    # Thresholds for load levels
    LOAD_THRESHOLDS = {
        CognitiveLoadLevel.VERY_LOW: 20,
        CognitiveLoadLevel.LOW: 40,
        CognitiveLoadLevel.OPTIMAL: 60,
        CognitiveLoadLevel.HIGH: 80,
        CognitiveLoadLevel.OVERLOAD: 100,
    }
    
    def __init__(self):
        self.baseline_metrics: Dict[int, Dict] = {}
    
    def establish_baseline(
        self,
        student_id: int,
        historical_data: List[Dict],
    ) -> Dict[str, float]:
        """
        Establish baseline metrics for a student.
        
        Args:
            student_id: Student ID
            historical_data: Past performance data
        
        Returns:
            Baseline metrics dictionary
        """
        if not historical_data:
            # Default baseline
            baseline = {
                "avg_response_time": 30.0,
                "avg_error_rate": 0.15,
                "avg_help_requests": 1.0,
            }
        else:
            # Calculate from history
            response_times = [d.get("response_time", 30) for d in historical_data]
            error_rates = [d.get("error_rate", 0.15) for d in historical_data]
            help_requests = [d.get("help_requests", 1) for d in historical_data]
            
            baseline = {
                "avg_response_time": statistics.mean(response_times),
                "avg_error_rate": statistics.mean(error_rates),
                "avg_help_requests": statistics.mean(help_requests),
            }
        
        self.baseline_metrics[student_id] = baseline
        return baseline
    
    def assess_cognitive_load(
        self,
        student_id: int,
        current_session: Dict,
        recent_context: List[Dict],
    ) -> CognitiveLoadAssessment:
        """
        Assess current cognitive load.
        
        Args:
            student_id: Student ID
            current_session: Current session data
            recent_context: Recent sessions for context
        
        Returns:
            CognitiveLoadAssessment with recommendations
        """
        # Ensure baseline exists
        if student_id not in self.baseline_metrics:
            self.establish_baseline(student_id, recent_context)
        
        baseline = self.baseline_metrics[student_id]
        
        # Calculate indicators
        indicators = self._calculate_indicators(
            current_session, baseline, recent_context
        )
        
        # Calculate load score
        load_score = self._calculate_load_score(indicators)
        
        # Determine load level
        current_load = self._score_to_load_level(load_score)
        
        # Analyze load components
        breakdown = self._analyze_load_breakdown(
            current_session, indicators, recent_context
        )
        
        # Generate recommendations
        action, adjustment, break_needed = self._generate_recommendations(
            current_load, indicators, breakdown
        )
        
        return CognitiveLoadAssessment(
            student_id=student_id,
            current_load=current_load,
            load_score=round(load_score, 1),
            indicators=indicators,
            breakdown=breakdown,
            recommended_action=action,
            difficulty_adjustment=round(adjustment, 2),
            break_recommended=break_needed,
            timestamp=current_session.get("timestamp", ""),
        )
    
    def _calculate_indicators(
        self,
        session: Dict,
        baseline: Dict,
        context: List[Dict],
    ) -> LoadIndicators:
        """Calculate cognitive load indicators."""
        # Error rate
        error_rate = session.get("error_rate", baseline["avg_error_rate"])
        
        # Response time increase
        current_rt = session.get("response_time", baseline["avg_response_time"])
        rt_increase = ((current_rt - baseline["avg_response_time"]) 
                        / baseline["avg_response_time"]) * 100
        
        # Help requests
        help_requests = session.get("help_requests", 0)
        
        # Pause frequency (pauses per minute)
        duration = session.get("duration_minutes", 1)
        pause_count = len(session.get("pauses", []))
        pause_freq = pause_count / duration
        
        # Revisions
        revisions = session.get("revisions", 0)
        
        # Hesitations (can be detected from keystroke patterns)
        hesitations = session.get("hesitation_count", 0)
        
        # Gaze and keystroke (if available)
        gaze_complexity = session.get("gaze_complexity", 0.5)
        keystroke = session.get("keystroke_dynamics", 1.0)
        
        return LoadIndicators(
            error_rate=round(error_rate, 3),
            response_time_increase=round(rt_increase, 1),
            help_requests=help_requests,
            pause_frequency=round(pause_freq, 2),
            revision_count=revisions,
            hesitation_count=hesitations,
            gaze_pattern_complexity=round(gaze_complexity, 2),
            keystroke_dynamics=round(keystroke, 2),
        )
    
    def _calculate_load_score(self, indicators: LoadIndicators) -> float:
        """Calculate overall cognitive load score (0-100)."""
        # Weighted scoring
        weights = {
            "error_rate": 0.25,
            "response_time": 0.20,
            "help_requests": 0.15,
            "pauses": 0.15,
            "revisions": 0.10,
            "hesitations": 0.10,
            "keystroke": 0.05,
        }
        
        # Normalize each indicator to 0-100
        error_score = min(100, indicators.error_rate * 500)  # 20% error = 100
        rt_score = max(0, min(100, indicators.response_time_increase))
        help_score = min(100, indicators.help_requests * 20)  # 5 requests = 100
        pause_score = min(100, indicators.pause_frequency * 50)  # 2/min = 100
        revision_score = min(100, indicators.revision_count * 20)
        hesitation_score = min(100, indicators.hesitation_count * 5)
        keystroke_score = max(0, min(100, (indicators.keystroke_dynamics - 1) * 50))
        
        # Weighted sum
        total_score = (
            error_score * weights["error_rate"] +
            rt_score * weights["response_time"] +
            help_score * weights["help_requests"] +
            pause_score * weights["pauses"] +
            revision_score * weights["revisions"] +
            hesitation_score * weights["hesitations"] +
            keystroke_score * weights["keystroke"]
        )
        
        return total_score
    
    def _score_to_load_level(self, score: float) -> CognitiveLoadLevel:
        """Convert load score to level."""
        if score < self.LOAD_THRESHOLDS[CognitiveLoadLevel.VERY_LOW]:
            return CognitiveLoadLevel.VERY_LOW
        elif score < self.LOAD_THRESHOLDS[CognitiveLoadLevel.LOW]:
            return CognitiveLoadLevel.LOW
        elif score < self.LOAD_THRESHOLDS[CognitiveLoadLevel.OPTIMAL]:
            return CognitiveLoadLevel.OPTIMAL
        elif score < self.LOAD_THRESHOLDS[CognitiveLoadLevel.HIGH]:
            return CognitiveLoadLevel.HIGH
        else:
            return CognitiveLoadLevel.OVERLOAD
    
    def _analyze_load_breakdown(
        self,
        session: Dict,
        indicators: LoadIndicators,
        context: List[Dict],
    ) -> Dict[LoadType, float]:
        """Analyze breakdown of load types."""
        # Intrinsic load (based on content complexity)
        concept_difficulty = session.get("concept_difficulty", 0.5)
        intrinsic = concept_difficulty * 100
        
        # Extraneous load (unnecessary load)
        # High due to poor instruction, distractions, etc.
        extraneous = 0
        if indicators.pause_frequency > 1:  # Frequent pauses
            extraneous += 20
        if session.get("distractions", 0) > 0:
            extraneous += 15
        if session.get("interface_issues", 0) > 0:
            extraneous += 20
        extraneous = min(100, extraneous)
        
        # Germane load (beneficial processing)
        # Schema construction, deep processing
        germane = 0
        if indicators.revision_count > 0:  # Self-correction
            germane += 30
        if session.get("elaboration_count", 0) > 0:  # Adding details
            germane += 25
        if session.get("connection_making", False):  # Linking concepts
            germane += 25
        germane = min(100, germane)
        
        return {
            LoadType.INTRINSIC: round(intrinsic, 1),
            LoadType.EXTRANEOUS: round(extraneous, 1),
            LoadType.GERMANE: round(germane, 1),
        }
    
    def _generate_recommendations(
        self,
        load_level: CognitiveLoadLevel,
        indicators: LoadIndicators,
        breakdown: Dict[LoadType, float],
    ) -> tuple:
        """Generate recommendations based on load."""
        actions = {
            CognitiveLoadLevel.VERY_LOW: (
                "Increase challenge - student may be bored",
                0.2,  # Increase difficulty
                False
            ),
            CognitiveLoadLevel.LOW: (
                "Maintain current pace - student is comfortable",
                0.0,
                False
            ),
            CognitiveLoadLevel.OPTIMAL: (
                "Optimal learning zone - continue as planned",
                0.0,
                False
            ),
            CognitiveLoadLevel.HIGH: (
                "Monitor closely - provide scaffolding if needed",
                -0.1,
                False
            ),
            CognitiveLoadLevel.OVERLOAD: (
                "Reduce cognitive load immediately - break or simplify",
                -0.3,
                True
            ),
        }
        
        action, adjustment, break_needed = actions.get(load_level, ("Continue", 0.0, False))
        
        # Refine based on breakdown
        if breakdown[LoadType.EXTRANEOUS] > 30:
            action += " - Reduce distractions and simplify interface"
        
        if breakdown[LoadType.GERMANE] < 20:
            action += " - Encourage deeper processing and reflection"
        
        return action, adjustment, break_needed
    
    def get_load_history_analysis(
        self,
        assessments: List[CognitiveLoadAssessment],
    ) -> Dict[str, any]:
        """Analyze history of cognitive load assessments."""
        if not assessments:
            return {"error": "No assessments available"}
        
        load_scores = [a.load_score for a in assessments]
        levels = [a.current_load for a in assessments]
        
        # Calculate time in each load level
        level_times = {}
        for level in CognitiveLoadLevel:
            count = levels.count(level)
            level_times[level.value] = {
                "count": count,
                "percentage": round(count / len(levels) * 100, 1),
            }
        
        # Trend analysis
        if len(load_scores) >= 3:
            first_avg = statistics.mean(load_scores[:3])
            last_avg = statistics.mean(load_scores[-3:])
            trend = "increasing" if last_avg > first_avg * 1.1 else \
                    "decreasing" if last_avg < first_avg * 0.9 else "stable"
        else:
            trend = "insufficient_data"
        
        # Optimal learning time
        optimal_count = levels.count(CognitiveLoadLevel.OPTIMAL)
        optimal_percentage = round(optimal_count / len(levels) * 100, 1)
        
        return {
            "total_assessments": len(assessments),
            "average_load": round(statistics.mean(load_scores), 1),
            "load_distribution": level_times,
            "trend": trend,
            "time_in_optimal_zone": f"{optimal_percentage}%",
            "recommendations": [
                "Schedule learning during optimal energy times" if optimal_percentage < 30 else None,
                "Reduce session complexity" if level_times.get(CognitiveLoadLevel.OVERLOAD.value, {}).get("percentage", 0) > 20 else None,
                "Increase challenge variety" if level_times.get(CognitiveLoadLevel.VERY_LOW.value, {}).get("percentage", 0) > 30 else None,
            ],
        }
    
    def suggest_cognitive_load_reduction(
        self,
        assessment: CognitiveLoadAssessment,
    ) -> List[str]:
        """Suggest specific ways to reduce cognitive load."""
        suggestions = []
        
        if assessment.current_load == CognitiveLoadLevel.OVERLOAD:
            suggestions.append("🛑 Take a 5-minute break immediately")
            suggestions.append("📝 Simplify the current problem - break it into smaller steps")
            suggestions.append("🎯 Review prerequisite concepts before continuing")
        
        if assessment.indicators.error_rate > 0.3:
            suggestions.append("📚 Switch to worked examples instead of practice problems")
        
        if assessment.indicators.response_time_increase > 50:
            suggestions.append("⏱️ Provide more time - don't rush to next concept")
        
        if assessment.indicators.help_requests > 3:
            suggestions.append("💡 Enable hints or provide partial solutions")
        
        if assessment.breakdown[LoadType.EXTRANEOUS] > 30:
            suggestions.append("🎨 Simplify the interface - remove visual clutter")
            suggestions.append("🔕 Minimize distractions and notifications")
        
        return suggestions if suggestions else ["✅ Current load is manageable"]


def monitor_student_cognitive_load(
    student_id: int,
    session_data: Dict,
    context_history: List[Dict],
) -> Dict[str, any]:
    """
    Main API-facing function for cognitive load monitoring.
    
    Args:
        student_id: Student ID
        session_data: Current session metrics
        context_history: Recent session history
    
    Returns:
        Cognitive load assessment as dictionary
    """
    monitor = CognitiveLoadMonitor()
    
    # Establish baseline if needed
    if not context_history:
        monitor.establish_baseline(student_id, [session_data])
    
    # Assess load
    assessment = monitor.assess_cognitive_load(
        student_id, session_data, context_history
    )
    
    # Get reduction suggestions if needed
    suggestions = []
    if assessment.current_load in [CognitiveLoadLevel.HIGH, CognitiveLoadLevel.OVERLOAD]:
        suggestions = monitor.suggest_cognitive_load_reduction(assessment)
    
    return {
        "student_id": assessment.student_id,
        "cognitive_load_level": assessment.current_load.value,
        "load_score": assessment.load_score,
        "indicators": {
            "error_rate": assessment.indicators.error_rate,
            "response_time_increase": assessment.indicators.response_time_increase,
            "help_requests": assessment.indicators.help_requests,
            "pause_frequency": assessment.indicators.pause_frequency,
        },
        "load_breakdown": {
            k.value: v for k, v in assessment.breakdown.items()
        },
        "recommendations": {
            "action": assessment.recommended_action,
            "difficulty_adjustment": assessment.difficulty_adjustment,
            "break_recommended": assessment.break_recommended,
        },
        "reduction_suggestions": suggestions,
        "timestamp": assessment.timestamp,
    }
