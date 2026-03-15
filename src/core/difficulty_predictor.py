"""
Difficulty Prediction Model

Dynamically adjusts problem difficulty based on student performance.
Uses Item Response Theory (IRT) concepts and adaptive algorithms.

Research Applications:
- Computerized Adaptive Testing (CAT)
- Personalized difficulty calibration
- Learning curve analysis
- Zone of Proximal Development (ZPD) estimation
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum
import math


class DifficultyModel(Enum):
    IRT_1PL = "irt_1pl"  # 1-parameter logistic
    IRT_2PL = "irt_2pl"  # 2-parameter logistic
    ELO_BASED = "elo_based"  # Chess rating inspired


@dataclass
class ProblemDifficulty:
    """Estimated difficulty of a problem."""
    problem_id: str
    difficulty_parameter: float  # b parameter in IRT
    discrimination: float  # a parameter in IRT (for 2PL)
    concept_requirements: List[str]
    estimated_success_rate: float
    optimal_ability_range: Tuple[float, float]


@dataclass
class StudentAbility:
    """Estimated ability level of a student."""
    student_id: int
    theta: float  # Ability estimate (-4 to 4)
    theta_se: float  # Standard error
    reliability: float
    concept_abilities: Dict[str, float]  # Per-concept ability


@dataclass
class PredictionResult:
    """Result of difficulty prediction."""
    recommended_difficulty: float
    confidence: float
    reasoning: str
    estimated_success_probability: float
    alternative_problems: List[str]
    adapt_to_zpd: bool  # Zone of Proximal Development


class DifficultyPredictor:
    """
    Adaptive difficulty prediction using IRT-inspired algorithms.
    
    Key concepts:
    - Student ability (theta) estimates
    - Problem difficulty (b) parameters
    - Discrimination (a) parameters
    - Information functions for optimal selection
    """
    
    def __init__(self, model: DifficultyModel = DifficultyModel.IRT_2PL):
        self.model = model
        self.min_theta = -4.0
        self.max_theta = 4.0
    
    def estimate_student_ability(
        self,
        student_id: int,
        response_history: List[Dict],
    ) -> StudentAbility:
        """
        Estimate student ability using Maximum Likelihood Estimation.
        
        Args:
            student_id: Student ID
            response_history: List of (problem_difficulty, correct) tuples
        
        Returns:
            StudentAbility with theta estimate
        """
        if not response_history:
            return StudentAbility(
                student_id=student_id,
                theta=0.0,
                theta_se=2.0,
                reliability=0.0,
                concept_abilities={},
            )
        
        # Simple ability estimation via mean performance
        # In production, would use MLE or Bayesian estimation
        correct_count = sum(1 for r in response_history if r.get("correct", False))
        total = len(response_history)
        
        # Convert to theta scale (-4 to 4)
        proportion = correct_count / total
        theta = self.min_theta + proportion * (self.max_theta - self.min_theta)
        
        # Calculate standard error (simplified)
        se = 1.0 / math.sqrt(max(1, total))
        
        # Calculate reliability
        reliability = 1 - (se ** 2 / 4)
        
        # Calculate per-concept abilities
        concept_responses: Dict[str, List[bool]] = {}
        for response in response_history:
            concept = response.get("concept_id", "general")
            if concept not in concept_responses:
                concept_responses[concept] = []
            concept_responses[concept].append(response.get("correct", False))
        
        concept_abilities = {}
        for concept, responses in concept_responses.items():
            concept_correct = sum(responses)
            concept_prop = concept_correct / len(responses)
            concept_abilities[concept] = self.min_theta + concept_prop * (self.max_theta - self.min_theta)
        
        return StudentAbility(
            student_id=student_id,
            theta=round(theta, 3),
            theta_se=round(se, 3),
            reliability=round(reliability, 3),
            concept_abilities=concept_abilities,
        )
    
    def predict_optimal_difficulty(
        self,
        student_ability: StudentAbility,
        available_problems: List[ProblemDifficulty],
        target_success_rate: float = 0.7,
    ) -> PredictionResult:
        """
        Predict optimal difficulty for a student.
        
        Uses information function to find problems that best
        discriminate at the student's ability level.
        
        Args:
            student_ability: Current ability estimate
            available_problems: List of available problems
            target_success_rate: Desired probability of success
        
        Returns:
            PredictionResult with recommendation
        """
        if not available_problems:
            return PredictionResult(
                recommended_difficulty=0.0,
                confidence=0.0,
                reasoning="No problems available",
                estimated_success_probability=0.5,
                alternative_problems=[],
                adapt_to_zpd=True,
            )
        
        # Calculate success probability for each problem
        problem_scores = []
        for problem in available_problems:
            success_prob = self._calculate_success_probability(
                student_ability.theta,
                problem.difficulty_parameter,
                problem.discrimination,
            )
            
            # Score based on closeness to target success rate
            # and information (discrimination)
            success_match = 1 - abs(success_prob - target_success_rate)
            information = self._calculate_information(
                student_ability.theta,
                problem.difficulty_parameter,
                problem.discrimination,
            )
            
            score = success_match * 0.6 + information * 0.4
            
            problem_scores.append((problem, score, success_prob))
        
        # Sort by score
        problem_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Select best problem
        best_problem, best_score, best_prob = problem_scores[0]
        
        # Get alternatives
        alternatives = [p[0].problem_id for p in problem_scores[1:4]]
        
        # Determine if we should adapt to ZPD
        # ZPD is typically slightly above current ability
        adapt_zpd = student_ability.theta > -2.0  # Not struggling too much
        
        # Generate reasoning
        if best_prob > target_success_rate + 0.2:
            reasoning = "Selected slightly easier problem to build confidence"
        elif best_prob < target_success_rate - 0.2:
            reasoning = "Selected challenging problem to stretch abilities"
        else:
            reasoning = "Selected problem in optimal difficulty zone for learning"
        
        return PredictionResult(
            recommended_difficulty=best_problem.difficulty_parameter,
            confidence=round(best_score, 3),
            reasoning=reasoning,
            estimated_success_probability=round(best_prob, 3),
            alternative_problems=alternatives,
            adapt_to_zpd=adapt_zpd,
        )
    
    def calculate_problem_difficulty(
        self,
        problem_id: str,
        response_data: List[Dict],
    ) -> ProblemDifficulty:
        """
        Calculate difficulty parameters for a problem.
        
        Args:
            problem_id: Problem ID
            response_data: List of student responses
        
        Returns:
            ProblemDifficulty with estimated parameters
        """
        if not response_data:
            return ProblemDifficulty(
                problem_id=problem_id,
                difficulty_parameter=0.0,
                discrimination=1.0,
                concept_requirements=[],
                estimated_success_rate=0.5,
                optimal_ability_range=(-1.0, 1.0),
            )
        
        # Calculate empirical difficulty
        correct_count = sum(1 for r in response_data if r.get("correct", False))
        total_count = len(response_data)
        success_rate = correct_count / total_count
        
        # Convert to difficulty parameter (higher = harder)
        # Use inverse logit transformation
        if success_rate == 0:
            difficulty = self.max_theta
        elif success_rate == 1:
            difficulty = self.min_theta
        else:
            # Simplified IRT difficulty estimation
            difficulty = -math.log(success_rate / (1 - success_rate))
            difficulty = max(self.min_theta, min(self.max_theta, difficulty))
        
        # Estimate discrimination (simplified)
        # In practice, would use more sophisticated methods
        discrimination = 1.0  # Default
        
        # Get concept requirements
        concepts = list(set(
            r.get("concept_id", "general") for r in response_data
        ))
        
        # Calculate optimal ability range
        optimal_range = (difficulty - 1.0, difficulty + 1.0)
        
        return ProblemDifficulty(
            problem_id=problem_id,
            difficulty_parameter=round(difficulty, 3),
            discrimination=round(discrimination, 3),
            concept_requirements=concepts,
            estimated_success_rate=round(success_rate, 3),
            optimal_ability_range=optimal_range,
        )
    
    def _calculate_success_probability(
        self,
        theta: float,
        difficulty: float,
        discrimination: float = 1.0,
    ) -> float:
        """
        Calculate probability of success using IRT 2PL model.
        
        P(theta) = 1 / (1 + exp(-a * (theta - b)))
        """
        exponent = -discrimination * (theta - difficulty)
        return 1.0 / (1.0 + math.exp(exponent))
    
    def _calculate_information(
        self,
        theta: float,
        difficulty: float,
        discrimination: float = 1.0,
    ) -> float:
        """
        Calculate item information function.
        
        Information is highest when difficulty matches ability.
        """
        p = self._calculate_success_probability(theta, difficulty, discrimination)
        return discrimination ** 2 * p * (1 - p)
    
    def get_zone_of_proximal_development(
        self,
        student_ability: StudentAbility,
    ) -> Tuple[float, float]:
        """
        Calculate Zone of Proximal Development (ZPD).
        
        ZPD is the range where student can succeed with scaffolding.
        Typically slightly above current ability.
        
        Returns:
            (min_difficulty, max_difficulty) tuple
        """
        # ZPD is approximately 0.5 to 1.0 logits above current ability
        zpd_min = student_ability.theta + 0.3
        zpd_max = student_ability.theta + 1.2
        
        return (zpd_min, zpd_max)
    
    def adapt_difficulty_realtime(
        self,
        current_theta: float,
        last_response_correct: bool,
        last_problem_difficulty: float,
        adaptation_rate: float = 0.3,
    ) -> float:
        """
        Real-time difficulty adaptation based on last response.
        
        Args:
            current_theta: Current ability estimate
            last_response_correct: Whether last answer was correct
            last_problem_difficulty: Difficulty of last problem
            adaptation_rate: How fast to adapt
        
        Returns:
            New recommended difficulty
        """
        if last_response_correct:
            # Increase difficulty slightly
            new_difficulty = last_problem_difficulty + adaptation_rate
        else:
            # Decrease difficulty
            new_difficulty = last_problem_difficulty - adaptation_rate * 1.5
        
        # Keep within bounds
        return max(self.min_theta, min(self.max_theta, new_difficulty))
    
    def generate_difficulty_report(
        self,
        student_ability: StudentAbility,
        problem_pool: List[ProblemDifficulty],
    ) -> Dict[str, any]:
        """Generate comprehensive difficulty analysis report."""
        
        # Categorize problems by difficulty
        categories = {
            "too_easy": [],
            "just_right": [],
            "challenging": [],
            "too_hard": [],
        }
        
        zpd_min, zpd_max = self.get_zone_of_proximal_development(student_ability)
        
        for problem in problem_pool:
            if problem.difficulty_parameter < zpd_min - 0.5:
                categories["too_easy"].append(problem.problem_id)
            elif problem.difficulty_parameter < zpd_min:
                categories["just_right"].append(problem.problem_id)
            elif problem.difficulty_parameter <= zpd_max:
                categories["challenging"].append(problem.problem_id)
            else:
                categories["too_hard"].append(problem.problem_id)
        
        return {
            "student_ability": {
                "theta": student_ability.theta,
                "reliability": student_ability.reliability,
            },
            "zone_of_proximal_development": {
                "min": round(zpd_min, 2),
                "max": round(zpd_max, 2),
            },
            "problem_distribution": {
                k: len(v) for k, v in categories.items()
            },
            "recommended_focus": "challenging" if len(categories["challenging"]) > 5 else "just_right",
            "optimal_success_rate": "70-80%",
        }


def predict_optimal_problem_difficulty(
    student_id: int,
    past_performance: List[Dict],
    available_problems: List[Dict],
) -> Dict[str, any]:
    """
    Main API-facing function for difficulty prediction.
    
    Args:
        student_id: Student ID
        past_performance: List of past problem attempts
        available_problems: List of available problems with metadata
    
    Returns:
        Prediction result with recommended difficulty
    """
    predictor = DifficultyPredictor()
    
    # Estimate student ability
    ability = predictor.estimate_student_ability(student_id, past_performance)
    
    # Convert available problems to ProblemDifficulty objects
    problem_objects = []
    for prob in available_problems:
        problem_objects.append(ProblemDifficulty(
            problem_id=prob.get("id", ""),
            difficulty_parameter=prob.get("difficulty", 0.0),
            discrimination=prob.get("discrimination", 1.0),
            concept_requirements=prob.get("concepts", []),
            estimated_success_rate=0.5,
            optimal_ability_range=(-1.0, 1.0),
        ))
    
    # Get prediction
    prediction = predictor.predict_optimal_difficulty(
        ability,
        problem_objects,
    )
    
    return {
        "student_ability_theta": ability.theta,
        "recommended_difficulty": prediction.recommended_difficulty,
        "confidence": prediction.confidence,
        "reasoning": prediction.reasoning,
        "estimated_success_rate": prediction.estimated_success_probability,
        "alternative_problems": prediction.alternative_problems,
        "adapt_to_zpd": prediction.adapt_to_zpd,
    }
