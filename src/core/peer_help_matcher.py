"""
Intelligent Peer Help Matching System

Matches students who need help with those who can provide it.
Uses collaborative filtering and expertise modeling.

Research Applications:
- Peer learning effectiveness
- Collaborative problem solving
- Knowledge transfer between peers
- Community-driven education
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import statistics
from datetime import datetime, timedelta


class HelpRequestStatus(Enum):
    """Status of help requests."""
    OPEN = "open"
    MATCHED = "matched"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    EXPIRED = "expired"


class ExpertiseLevel(Enum):
    """Expertise levels for helping."""
    NOVICE = "novice"           # Can help with basics
    INTERMEDIATE = "intermediate"  # Can help with most topics
    EXPERT = "expert"           # Can help with advanced topics
    MENTOR = "mentor"           # Can mentor others


@dataclass
class StudentProfile:
    """Profile for peer matching."""
    student_id: int
    name: str
    strong_concepts: List[str]
    weak_concepts: List[str]
    help_given_count: int
    help_received_count: int
    avg_help_rating: float
    learning_style: str
    availability: List[str]  # ["morning", "afternoon", "evening"]
    preferred_communication: str  # "chat", "video", "async"
    timezone: str


@dataclass
class HelpRequest:
    """Request for help."""
    request_id: str
    student_id: int
    concept_id: str
    concept_name: str
    difficulty_level: int
    description: str
    status: HelpRequestStatus
    created_at: datetime
    matched_helper: Optional[int] = None
    expiration: Optional[datetime] = None


@dataclass
class MatchResult:
    """Result of matching."""
    request: HelpRequest
    matched_helper: StudentProfile
    match_score: float
    match_reasons: List[str]
    estimated_success_rate: float


class PeerHelpMatcher:
    """
    Intelligent matcher for peer help.
    
    Algorithm:
    1. Expertise matching: Helper strong in requested concept
    2. Complementary matching: Different learning styles can help
    3. Recency matching: Avoid recently helped pairs
    4. Rating matching: Prioritize highly-rated helpers
    """
    
    def __init__(self):
        self.min_match_score = 0.6
        self.max_concurrent_helps = 3
    
    def find_helpers(
        self,
        request: HelpRequest,
        candidate_helpers: List[StudentProfile],
        recent_matches: List[tuple],  # [(helper_id, timestamp)]
    ) -> List[MatchResult]:
        """
        Find best matching helpers for a request.
        
        Args:
            request: The help request
            candidate_helpers: Available helpers
            recent_matches: Recent match history
        
        Returns:
            List of match results, sorted by score
        """
        matches = []
        
        # Calculate recency penalty
        recent_helper_ids = {h for h, _ in recent_matches[-10:]}
        
        for helper in candidate_helpers:
            # Skip self-matching
            if helper.student_id == request.student_id:
                continue
            
            # Skip if at help capacity
            if helper.help_given_count >= self.max_concurrent_helps:
                continue
            
            # Calculate match score
            score, reasons = self._calculate_match_score(
                request, helper, recent_helper_ids
            )
            
            if score >= self.min_match_score:
                # Estimate success rate
                success_rate = self._estimate_success_rate(
                    request, helper, score
                )
                
                matches.append(MatchResult(
                    request=request,
                    matched_helper=helper,
                    match_score=score,
                    match_reasons=reasons,
                    estimated_success_rate=success_rate,
                ))
        
        # Sort by score
        matches.sort(key=lambda m: m.match_score, reverse=True)
        return matches
    
    def _calculate_match_score(
        self,
        request: HelpRequest,
        helper: StudentProfile,
        recent_helpers: set,
    ) -> tuple:
        """Calculate match score between request and helper."""
        scores = []
        reasons = []
        
        # 1. Expertise match (40%)
        concept = request.concept_id
        if concept in helper.strong_concepts:
            scores.append(0.4)
            reasons.append(f"Expert in {request.concept_name}")
        elif any(c in helper.strong_concepts for c in ["programming", "python"]):
            scores.append(0.2)
            reasons.append("Strong programming background")
        
        # 2. Complementary learning styles (20%)
        if helper.learning_style != "similar":  # Assume requester has different style
            scores.append(0.2)
            reasons.append("Complementary learning perspective")
        
        # 3. Help rating (20%)
        if helper.avg_help_rating >= 4.5:
            scores.append(0.2)
            reasons.append("Highly rated helper (4.5+)")
        elif helper.avg_help_rating >= 4.0:
            scores.append(0.15)
            reasons.append("Well-rated helper")
        
        # 4. Experience balance (10%)
        if helper.help_given_count > 5 and helper.help_given_count < 50:
            scores.append(0.1)
            reasons.append("Experienced but not overwhelmed")
        
        # 5. Recency penalty (10%)
        if helper.student_id in recent_helpers:
            scores.append(0.05)
            reasons.append("Recently matched (variety)")
        else:
            scores.append(0.1)
            reasons.append("Fresh match")
        
        total_score = sum(scores)
        return total_score, reasons
    
    def _estimate_success_rate(
        self,
        request: HelpRequest,
        helper: StudentProfile,
        match_score: float,
    ) -> float:
        """Estimate probability of successful help."""
        base_rate = 0.7
        
        # Adjust by match score
        rate = base_rate + (match_score - 0.6) * 0.3
        
        # Adjust by helper rating
        rate += (helper.avg_help_rating - 4.0) * 0.05
        
        # Adjust by difficulty
        difficulty_factor = 1 - (request.difficulty_level - 1) * 0.05
        rate *= difficulty_factor
        
        return min(0.95, max(0.5, rate))
    
    def create_help_session(
        self,
        match: MatchResult,
        session_type: str = "interactive",
    ) -> Dict:
        """Create a help session from a match."""
        return {
            "session_id": f"hs_{match.request.request_id}_{match.matched_helper.student_id}",
            "request_id": match.request.request_id,
            "helper_id": match.matched_helper.student_id,
            "helped_id": match.request.student_id,
            "concept": match.request.concept_name,
            "match_score": match.match_score,
            "estimated_success": match.estimated_success_rate,
            "session_type": session_type,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending",
            "suggested_approach": self._suggest_approach(match),
        }
    
    def _suggest_approach(self, match: MatchResult) -> List[str]:
        """Suggest teaching approach based on match."""
        suggestions = []
        
        # Based on expertise
        if match.match_score > 0.85:
            suggestions.append("Use Socratic questioning - guide to discovery")
        elif match.match_score > 0.7:
            suggestions.append("Provide worked examples with explanations")
        else:
            suggestions.append("Start with basics and build up gradually")
        
        # Based on learning styles
        if "Complementary" in match.match_reasons:
            suggestions.append("Share alternative perspective/approach")
        
        # Based on difficulty
        if match.request.difficulty_level >= 4:
            suggestions.append("Break into smaller sub-problems")
        
        return suggestions
    
    def analyze_help_network(
        self,
        all_students: List[StudentProfile],
        all_requests: List[HelpRequest],
        completed_sessions: List[Dict],
    ) -> Dict:
        """Analyze the help network for insights."""
        # Calculate network metrics
        total_requests = len(all_requests)
        resolved_requests = sum(1 for r in all_requests if r.status == HelpRequestStatus.RESOLVED)
        
        # Helper statistics
        top_helpers = sorted(
            all_students,
            key=lambda s: s.help_given_count,
            reverse=True
        )[:5]
        
        # Concept help frequency
        concept_requests: Dict[str, int] = {}
        for req in all_requests:
            concept_requests[req.concept_id] = concept_requests.get(req.concept_id, 0) + 1
        
        most_helped_concepts = sorted(
            concept_requests.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Success rate
        if completed_sessions:
            ratings = [s.get("rating", 0) for s in completed_sessions if s.get("rating")]
            avg_rating = statistics.mean(ratings) if ratings else 0
        else:
            avg_rating = 0
        
        return {
            "network_stats": {
                "total_requests": total_requests,
                "resolved_requests": resolved_requests,
                "resolution_rate": round(resolved_requests / total_requests, 2) if total_requests else 0,
                "active_helpers": len([s for s in all_students if s.help_given_count > 0]),
                "avg_help_rating": round(avg_rating, 2),
            },
            "top_helpers": [
                {
                    "student_id": h.student_id,
                    "name": h.name,
                    "help_given": h.help_given_count,
                    "avg_rating": h.avg_help_rating,
                }
                for h in top_helpers
            ],
            "most_helped_concepts": [
                {"concept_id": c[0], "request_count": c[1]}
                for c in most_helped_concepts
            ],
            "recommendations": [
                "Increase incentives for peer help" if resolved_requests / total_requests < 0.7 else None,
                f"Focus on {most_helped_concepts[0][0]} - most requested" if most_helped_concepts else None,
                "Recognize top helpers" if top_helpers and top_helpers[0].help_given_count > 10 else None,
            ],
        }
    
    def get_help_recommendations(
        self,
        student: StudentProfile,
        available_requests: List[HelpRequest],
    ) -> List[Dict]:
        """Recommend help opportunities for a student."""
        recommendations = []
        
        for request in available_requests:
            if request.student_id == student.student_id:
                continue
            
            # Check if student can help
            score, reasons = self._calculate_match_score(
                request, student, set()
            )
            
            if score >= 0.5:
                recommendations.append({
                    "request_id": request.request_id,
                    "concept": request.concept_name,
                    "difficulty": request.difficulty_level,
                    "match_score": score,
                    "reasons": reasons,
                    "estimated_time": self._estimate_help_time(request),
                })
        
        # Sort by match score
        recommendations.sort(key=lambda r: r["match_score"], reverse=True)
        return recommendations[:5]
    
    def _estimate_help_time(self, request: HelpRequest) -> int:
        """Estimate minutes needed to help."""
        base_time = 15
        difficulty_multiplier = request.difficulty_level
        return base_time * difficulty_multiplier


def match_peer_help(
    request_data: Dict,
    helper_profiles: List[Dict],
    recent_matches: Optional[List[tuple]] = None,
) -> Dict:
    """
    Main API-facing function for peer help matching.
    
    Args:
        request_data: Help request details
        helper_profiles: Available helpers
        recent_matches: Recent match history
    
    Returns:
        Match results with recommendations
    """
    matcher = PeerHelpMatcher()
    
    # Create request object
    request = HelpRequest(
        request_id=request_data.get("id", ""),
        student_id=request_data.get("student_id", 0),
        concept_id=request_data.get("concept_id", ""),
        concept_name=request_data.get("concept_name", ""),
        difficulty_level=request_data.get("difficulty", 1),
        description=request_data.get("description", ""),
        status=HelpRequestStatus.OPEN,
        created_at=datetime.utcnow(),
        expiration=datetime.utcnow() + timedelta(hours=24),
    )
    
    # Create helper profiles
    helpers = [
        StudentProfile(
            student_id=h.get("id", 0),
            name=h.get("name", ""),
            strong_concepts=h.get("strong_concepts", []),
            weak_concepts=h.get("weak_concepts", []),
            help_given_count=h.get("help_given", 0),
            help_received_count=h.get("help_received", 0),
            avg_help_rating=h.get("avg_rating", 4.0),
            learning_style=h.get("learning_style", "mixed"),
            availability=h.get("availability", ["afternoon"]),
            preferred_communication=h.get("communication", "chat"),
            timezone=h.get("timezone", "UTC"),
        )
        for h in helper_profiles
    ]
    
    # Find matches
    matches = matcher.find_helpers(request, helpers, recent_matches or [])
    
    return {
        "request_id": request.request_id,
        "matches_found": len(matches),
        "top_matches": [
            {
                "helper_id": m.matched_helper.student_id,
                "helper_name": m.matched_helper.name,
                "match_score": round(m.match_score, 2),
                "match_reasons": m.match_reasons,
                "estimated_success": round(m.estimated_success_rate, 2),
                "expertise_level": "expert" if m.match_score > 0.8 else "intermediate",
            }
            for m in matches[:3]
        ],
        "suggested_session": matcher.create_help_session(matches[0]) if matches else None,
    }
