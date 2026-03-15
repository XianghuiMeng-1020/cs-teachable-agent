"""
Peer Comparison System

Enables anonymous comparison of learning performance among students.
Provides insights through statistical analysis while maintaining privacy.

Research Applications:
- Social learning comparison effects
- Benchmarking and norm-referenced assessment
- Learning community dynamics
- Self-assessment calibration
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
import statistics


class ComparisonMetric(Enum):
    LEARNING_SPEED = "learning_speed"
    CONCEPT_MASTERY = "concept_mastery"
    TEST_PERFORMANCE = "test_performance"
    CONSISTENCY = "consistency"
    ENGAGEMENT = "engagement"
    HELP_GIVING = "help_giving"


@dataclass
class StudentSnapshot:
    """Anonymous snapshot of a student's performance."""
    student_id: int  # Hashed/anonymized
    percentile: float  # 0-100
    raw_value: float
    trend: str  # "improving", "stable", "declining"
    cohort_size: int


@dataclass
class ComparisonResult:
    """Result of peer comparison."""
    student_position: int  # Rank in cohort
    total_students: int
    percentile: float  # 0-100
    comparison_metric: str
    student_value: float
    average_value: float
    top_performer_value: float
    distribution: Dict[str, float]  # quartiles
    similar_students: List[StudentSnapshot]
    insights: List[str]
    recommendations: List[str]


@dataclass
class CohortStatistics:
    """Statistics for a group/cohort."""
    metric: str
    count: int
    mean: float
    median: float
    std_dev: float
    min: float
    max: float
    quartiles: Dict[str, float]


class PeerComparisonSystem:
    """
    System for anonymous peer comparison.
    
    Privacy features:
    - Student IDs are hashed
    - Minimum cohort size (5) to prevent identification
    - Only percentile rankings shown, not raw ranks
    """
    
    MIN_COHORT_SIZE = 5
    
    def __init__(self):
        pass
    
    def compare_learning_speed(
        self,
        student_id: int,
        concepts_per_day: float,
        cohort_data: List[Dict],
    ) -> ComparisonResult:
        """
        Compare learning speed (concepts learned per day).
        
        Args:
            student_id: Target student ID
            concepts_per_day: Student's learning rate
            cohort_data: List of other students' data
        
        Returns:
            Comparison result with percentile and insights
        """
        values = [d.get("concepts_per_day", 0) for d in cohort_data]
        values.append(concepts_per_day)
        
        stats = self._calculate_statistics(values)
        percentile = self._calculate_percentile(concepts_per_day, values)
        
        # Generate insights
        insights = []
        if percentile >= 80:
            insights.append("You're learning faster than 80% of your peers!")
        elif percentile >= 60:
            insights.append("Your learning pace is above average.")
        elif percentile >= 40:
            insights.append("Your learning pace is around average.")
        else:
            insights.append("You might benefit from slowing down to ensure understanding.")
        
        # Find similar students
        similar = self._find_similar_students(
            student_id, concepts_per_day, values, cohort_data
        )
        
        return ComparisonResult(
            student_position=self._get_rank(concepts_per_day, values),
            total_students=len(values),
            percentile=percentile,
            comparison_metric="learning_speed",
            student_value=round(concepts_per_day, 2),
            average_value=round(stats.mean, 2),
            top_performer_value=round(stats.max, 2),
            distribution=stats.quartiles,
            similar_students=similar,
            insights=insights,
            recommendations=self._generate_recommendations(percentile, "speed"),
        )
    
    def compare_mastery_level(
        self,
        student_id: int,
        mastery_scores: Dict[str, float],
        cohort_data: List[Dict],
    ) -> ComparisonResult:
        """Compare concept mastery levels."""
        avg_mastery = sum(mastery_scores.values()) / max(1, len(mastery_scores))
        
        cohort_mastery = []
        for student in cohort_data:
            scores = student.get("mastery_scores", {})
            if scores:
                cohort_mastery.append(sum(scores.values()) / len(scores))
        
        cohort_mastery.append(avg_mastery)
        
        stats = self._calculate_statistics(cohort_mastery)
        percentile = self._calculate_percentile(avg_mastery, cohort_mastery)
        
        insights = []
        if percentile >= 80:
            insights.append("Excellent mastery - you're among the top performers!")
        elif percentile >= 60:
            insights.append("Good mastery level. Keep practicing to improve retention.")
        elif percentile >= 40:
            insights.append("Average mastery. Consider reviewing older concepts.")
        else:
            insights.append("Focus on strengthening fundamentals before moving forward.")
        
        # Identify weak areas compared to peers
        weak_areas = []
        for concept, score in mastery_scores.items():
            peer_avg = sum(s.get("mastery_scores", {}).get(concept, 0) for s in cohort_data) / len(cohort_data)
            if score < peer_avg - 0.2:
                weak_areas.append(concept)
        
        if weak_areas:
            insights.append(f"Areas where peers are ahead: {', '.join(weak_areas[:3])}")
        
        return ComparisonResult(
            student_position=self._get_rank(avg_mastery, cohort_mastery),
            total_students=len(cohort_mastery),
            percentile=percentile,
            comparison_metric="mastery_level",
            student_value=round(avg_mastery * 100, 1),
            average_value=round(stats.mean * 100, 1),
            top_performer_value=round(stats.max * 100, 1),
            distribution={k: round(v * 100, 1) for k, v in stats.quartiles.items()},
            similar_students=[],
            insights=insights,
            recommendations=self._generate_recommendations(percentile, "mastery"),
        )
    
    def compare_consistency(
        self,
        student_id: int,
        activity_pattern: List[bool],
        cohort_data: List[Dict],
    ) -> ComparisonResult:
        """Compare learning consistency (streaks, regularity)."""
        # Calculate consistency score
        student_score = self._calculate_consistency_score(activity_pattern)
        
        cohort_scores = []
        for student in cohort_data:
            pattern = student.get("activity_pattern", [])
            if pattern:
                cohort_scores.append(self._calculate_consistency_score(pattern))
        
        cohort_scores.append(student_score)
        
        stats = self._calculate_statistics(cohort_scores)
        percentile = self._calculate_percentile(student_score, cohort_scores)
        
        insights = []
        if percentile >= 80:
            insights.append("Great consistency! Regular practice leads to better retention.")
        elif percentile >= 60:
            insights.append("Good consistency. Try to maintain your current schedule.")
        elif percentile >= 40:
            insights.append("Average consistency. Consider setting a regular study schedule.")
        else:
            insights.append("Inconsistent activity detected. Try studying at the same time each day.")
        
        return ComparisonResult(
            student_position=self._get_rank(student_score, cohort_scores),
            total_students=len(cohort_scores),
            percentile=percentile,
            comparison_metric="consistency",
            student_value=round(student_score, 1),
            average_value=round(stats.mean, 1),
            top_performer_value=round(stats.max, 1),
            distribution=stats.quartiles,
            similar_students=[],
            insights=insights,
            recommendations=self._generate_recommendations(percentile, "consistency"),
        )
    
    def generate_cohort_report(
        self,
        cohort_data: List[Dict],
        metric: ComparisonMetric,
    ) -> Dict[str, any]:
        """Generate aggregate report for a cohort."""
        if len(cohort_data) < self.MIN_COHORT_SIZE:
            return {
                "error": "Cohort too small for anonymous comparison",
                "minimum_required": self.MIN_COHORT_SIZE,
                "current_size": len(cohort_data),
            }
        
        values = []
        for student in cohort_data:
            if metric == ComparisonMetric.LEARNING_SPEED:
                values.append(student.get("concepts_per_day", 0))
            elif metric == ComparisonMetric.CONSISTENCY:
                pattern = student.get("activity_pattern", [])
                if pattern:
                    values.append(self._calculate_consistency_score(pattern))
            # Add other metrics...
        
        stats = self._calculate_statistics(values)
        
        return {
            "metric": metric.value,
            "cohort_size": len(cohort_data),
            "statistics": {
                "mean": round(stats.mean, 2),
                "median": round(stats.median, 2),
                "std_dev": round(stats.std_dev, 2),
                "range": f"{round(stats.min, 2)} - {round(stats.max, 2)}",
            },
            "distribution": {
                "top_25_percent": f">= {round(stats.quartiles['q3'], 2)}",
                "middle_50_percent": f"{round(stats.quartiles['q1'], 2)} - {round(stats.quartiles['q3'], 2)}",
                "bottom_25_percent": f"<= {round(stats.quartiles['q1'], 2)}",
            },
            "interpretation": self._interpret_distribution(stats),
        }
    
    def _calculate_statistics(self, values: List[float]) -> CohortStatistics:
        """Calculate statistical measures."""
        if not values:
            return CohortStatistics("", 0, 0, 0, 0, 0, 0, {})
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        return CohortStatistics(
            metric="",
            count=n,
            mean=statistics.mean(sorted_values),
            median=statistics.median(sorted_values),
            std_dev=statistics.stdev(sorted_values) if n > 1 else 0,
            min=min(sorted_values),
            max=max(sorted_values),
            quartiles={
                "q1": sorted_values[n // 4] if n >= 4 else sorted_values[0],
                "median": sorted_values[n // 2],
                "q3": sorted_values[3 * n // 4] if n >= 4 else sorted_values[-1],
            },
        )
    
    def _calculate_percentile(self, value: float, all_values: List[float]) -> float:
        """Calculate percentile rank."""
        if not all_values:
            return 50.0
        
        sorted_values = sorted(all_values)
        below = sum(1 for v in sorted_values if v < value)
        equal = sum(1 for v in sorted_values if v == value)
        
        return ((below + 0.5 * equal) / len(sorted_values)) * 100
    
    def _get_rank(self, value: float, all_values: List[float]) -> int:
        """Get rank (1-based) in sorted list."""
        sorted_desc = sorted(all_values, reverse=True)
        for i, v in enumerate(sorted_desc):
            if v <= value:
                return i + 1
        return len(sorted_desc)
    
    def _calculate_consistency_score(self, activity_pattern: List[bool]) -> float:
        """Calculate consistency score from activity pattern."""
        if not activity_pattern:
            return 0.0
        
        # Count streaks
        current_streak = 0
        max_streak = 0
        for active in activity_pattern:
            if active:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        
        # Calculate regularity (active days / total days)
        regularity = sum(activity_pattern) / len(activity_pattern)
        
        # Combine streak and regularity
        return (max_streak * 0.4 + regularity * 10 * 0.6)
    
    def _find_similar_students(
        self,
        student_id: int,
        student_value: float,
        all_values: List[float],
        cohort_data: List[Dict],
    ) -> List[StudentSnapshot]:
        """Find students with similar performance."""
        # Find values within 10% range
        similar = []
        for data in cohort_data:
            other_id = data.get("student_id")
            if other_id == student_id:
                continue
            
            other_value = data.get("concepts_per_day", 0)
            if abs(other_value - student_value) / max(student_value, 0.1) < 0.1:
                similar.append(StudentSnapshot(
                    student_id=other_id,  # Should be hashed
                    percentile=self._calculate_percentile(other_value, all_values),
                    raw_value=other_value,
                    trend=data.get("trend", "stable"),
                    cohort_size=len(all_values),
                ))
        
        return similar[:5]  # Return top 5 similar
    
    def _generate_recommendations(
        self,
        percentile: float,
        metric_type: str,
    ) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []
        
        if metric_type == "speed":
            if percentile < 40:
                recommendations.append("Focus on understanding rather than speed")
                recommendations.append("Break complex concepts into smaller parts")
            elif percentile > 80:
                recommendations.append("Consider teaching others to reinforce your learning")
        
        elif metric_type == "mastery":
            if percentile < 40:
                recommendations.append("Review fundamentals before advancing")
                recommendations.append("Use spaced repetition to improve retention")
            elif percentile > 80:
                recommendations.append("Challenge yourself with advanced topics")
        
        elif metric_type == "consistency":
            if percentile < 40:
                recommendations.append("Set a daily study reminder")
                recommendations.append("Start with 10-minute sessions to build habit")
            elif percentile > 80:
                recommendations.append("Maintain your excellent study routine!")
        
        return recommendations
    
    def _interpret_distribution(self, stats: CohortStatistics) -> str:
        """Interpret statistical distribution."""
        cv = stats.std_dev / stats.mean if stats.mean > 0 else 0
        
        if cv < 0.2:
            return "The cohort shows very consistent performance."
        elif cv < 0.4:
            return "The cohort shows moderate variation in performance."
        else:
            return "The cohort shows high variation - consider differentiated instruction."


def compare_with_peers(
    student_id: int,
    metric: str,
    student_value: float,
    cohort_data: List[Dict],
) -> ComparisonResult:
    """
    Convenience function for peer comparison.
    
    This is the main API-facing function.
    """
    pcs = PeerComparisonSystem()
    
    if metric == "learning_speed":
        return pcs.compare_learning_speed(student_id, student_value, cohort_data)
    elif metric == "mastery":
        return pcs.compare_mastery_level(student_id, {"general": student_value}, cohort_data)
    elif metric == "consistency":
        return pcs.compare_consistency(student_id, [True, False, True], cohort_data)
    else:
        raise ValueError(f"Unknown metric: {metric}")


def get_cohort_benchmarks(
    cohort_data: List[Dict],
) -> Dict[str, any]:
    """Get benchmark statistics for a cohort."""
    pcs = PeerComparisonSystem()
    
    return {
        "learning_speed": pcs.generate_cohort_report(
            cohort_data, ComparisonMetric.LEARNING_SPEED
        ),
        "consistency": pcs.generate_cohort_report(
            cohort_data, ComparisonMetric.CONSISTENCY
        ),
    }
