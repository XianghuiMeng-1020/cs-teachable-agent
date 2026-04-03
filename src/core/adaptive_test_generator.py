"""
Adaptive Test Generation System

Generates personalized test questions based on:
- Student's current knowledge state (BKT)
- Learning history and misconceptions
- Difficulty progression
- Knowledge gap identification

Research-backed adaptive testing using Item Response Theory (IRT) concepts.
"""

import random
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class QuestionDifficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


@dataclass
class KnowledgeGap:
    """Identified gap in student's knowledge."""
    unit_id: str
    gap_type: str  # 'untested', 'low_mastery', 'misconception_prone'
    severity: float  # 0.0 to 1.0
    recommended_difficulty: QuestionDifficulty
    prerequisites_needed: list[str]


@dataclass
class AdaptiveQuestion:
    """Generated adaptive test question."""
    question_id: str
    question_text: str
    target_knowledge_unit: str
    difficulty: QuestionDifficulty
    question_type: str  # 'conceptual', 'application', 'analysis'
    estimated_time_minutes: int
    hints: list[str]
    expected_answer_elements: list[str]
    misconception_traps: list[str]  # Common wrong answers to watch for


class AdaptiveTestGenerator:
    """Generates personalized tests using adaptive algorithms."""

    # Question templates by difficulty and domain
    QUESTION_TEMPLATES = {
        "python": {
            QuestionDifficulty.EASY: [
                {
                    "template": "What is the output of the following code?\n```python\n{code}\n```",
                    "type": "conceptual",
                    "time": 3,
                },
                {
                    "template": "Fill in the blank to make this code work:\n```python\n{code_with_blank}\n```",
                    "type": "application",
                    "time": 5,
                },
            ],
            QuestionDifficulty.MEDIUM: [
                {
                    "template": "Write a function that {requirement}. Your function should handle {edge_case}.",
                    "type": "application",
                    "time": 8,
                },
                {
                    "template": "Given the following code:\n```python\n{code}\n```\nWhat will happen when {scenario}? Explain your reasoning.",
                    "type": "analysis",
                    "time": 6,
                },
            ],
            QuestionDifficulty.HARD: [
                {
                    "template": "Design a solution for {complex_problem}. Consider {constraints}.",
                    "type": "analysis",
                    "time": 12,
                },
                {
                    "template": "Debug the following code that has {error_type}. Find and fix all issues:\n```python\n{buggy_code}\n```",
                    "type": "application",
                    "time": 10,
                },
            ],
            QuestionDifficulty.EXPERT: [
                {
                    "template": "Create an optimized solution for {advanced_problem}. Your solution should be {performance_requirement}.",
                    "type": "analysis",
                    "time": 15,
                },
            ],
        },
        "database": {
            QuestionDifficulty.EASY: [
                {
                    "template": "Write a SQL query to {simple_task} from the {table} table.",
                    "type": "conceptual",
                    "time": 3,
                },
            ],
            QuestionDifficulty.MEDIUM: [
                {
                    "template": "Write a SQL query that {complex_task} using {required_technique}.",
                    "type": "application",
                    "time": 8,
                },
            ],
            QuestionDifficulty.HARD: [
                {
                    "template": "Given these tables:\n{schema}\nWrite a query to solve {complex_query} with optimal performance.",
                    "type": "analysis",
                    "time": 12,
                },
            ],
            QuestionDifficulty.EXPERT: [
                {
                    "template": "Design a database schema for {complex_schema_design}. Include tables, relationships, indexes, and explain your design decisions.",
                    "type": "analysis",
                    "time": 15,
                },
            ],
        },
        "ai_literacy": {
            QuestionDifficulty.EASY: [
                {
                    "template": "What is {concept}? Explain in your own words.",
                    "type": "conceptual",
                    "time": 3,
                },
                {
                    "template": "List {number} common applications of {concept} in everyday life.",
                    "type": "conceptual",
                    "time": 5,
                },
            ],
            QuestionDifficulty.MEDIUM: [
                {
                    "template": "Compare {concept_a} and {concept_b}. What are the key differences and when would you use each?",
                    "type": "analysis",
                    "time": 8,
                },
                {
                    "template": "Given the scenario: {scenario}\nHow would you apply {concept} to solve this problem?",
                    "type": "application",
                    "time": 8,
                },
            ],
            QuestionDifficulty.HARD: [
                {
                    "template": "Analyze the following AI system description:\n{system_description}\nWhat are the potential ethical concerns? How would you address them?",
                    "type": "analysis",
                    "time": 12,
                },
                {
                    "template": "Design a prompt for {task} that accounts for {constraint}. Explain your prompt engineering choices.",
                    "type": "application",
                    "time": 10,
                },
            ],
            QuestionDifficulty.EXPERT: [
                {
                    "template": "Critically evaluate the following AI use case:\n{use_case}\nConsider: technical feasibility, ethical implications, societal impact, and mitigation strategies for risks.",
                    "type": "analysis",
                    "time": 15,
                },
            ],
        },
    }

    def __init__(self, domain: str = "python"):
        self.domain = domain
        self.templates = self.QUESTION_TEMPLATES.get(domain, self.QUESTION_TEMPLATES["python"])

    def identify_knowledge_gaps(
        self,
        knowledge_state: dict,
        learned_units: set,
        test_history: list[dict],
        misconceptions: list[str],
    ) -> list[KnowledgeGap]:
        """
        Identify gaps in student's knowledge for targeted testing.
        
        Returns prioritized list of knowledge gaps.
        """
        gaps = []
        
        for unit_id, state in knowledge_state.items():
            p_know = state.get("p_know", 0.0)
            
            # Check if this unit has been tested recently
            recently_tested = any(
                t.get("unit_id") == unit_id 
                for t in test_history[-5:]  # Last 5 tests
            )
            
            # Identify gap type and severity
            if unit_id not in learned_units:
                # Unit not learned yet
                if not recently_tested:
                    gaps.append(KnowledgeGap(
                        unit_id=unit_id,
                        gap_type="untested",
                        severity=0.5,
                        recommended_difficulty=QuestionDifficulty.EASY,
                        prerequisites_needed=[],
                    ))
            elif p_know < 0.6:
                # Low mastery despite learning
                gaps.append(KnowledgeGap(
                    unit_id=unit_id,
                    gap_type="low_mastery",
                    severity=1.0 - p_know,
                    recommended_difficulty=QuestionDifficulty.MEDIUM,
                    prerequisites_needed=[],
                ))
            elif unit_id in misconceptions:
                # Has active misconceptions
                gaps.append(KnowledgeGap(
                    unit_id=unit_id,
                    gap_type="misconception_prone",
                    severity=0.8,
                    recommended_difficulty=QuestionDifficulty.HARD,
                    prerequisites_needed=[],
                ))
            elif not recently_tested and p_know < 0.8:
                # Needs reinforcement
                gaps.append(KnowledgeGap(
                    unit_id=unit_id,
                    gap_type="needs_reinforcement",
                    severity=0.3,
                    recommended_difficulty=QuestionDifficulty.MEDIUM,
                    prerequisites_needed=[],
                ))
        
        # Sort by severity (descending)
        gaps.sort(key=lambda g: g.severity, reverse=True)
        
        return gaps

    def select_difficulty(
        self,
        p_know: float,
        gap_type: str,
        previous_attempts: int,
    ) -> QuestionDifficulty:
        """
        Select appropriate difficulty using adaptive algorithm.
        
        Uses modified 2PL IRT model concepts.
        """
        # Base difficulty from mastery
        if p_know < 0.4:
            base_difficulty = QuestionDifficulty.EASY
        elif p_know < 0.7:
            base_difficulty = QuestionDifficulty.MEDIUM
        elif p_know < 0.9:
            base_difficulty = QuestionDifficulty.HARD
        else:
            base_difficulty = QuestionDifficulty.EXPERT
        
        # Adjust based on gap type
        if gap_type == "misconception_prone":
            # Challenge misconceptions with harder questions
            difficulty_map = {
                QuestionDifficulty.EASY: QuestionDifficulty.MEDIUM,
                QuestionDifficulty.MEDIUM: QuestionDifficulty.HARD,
                QuestionDifficulty.HARD: QuestionDifficulty.EXPERT,
                QuestionDifficulty.EXPERT: QuestionDifficulty.EXPERT,
            }
            base_difficulty = difficulty_map.get(base_difficulty, base_difficulty)
        
        # Adjust based on attempt history
        if previous_attempts > 2:
            # Student struggling, reduce difficulty
            difficulty_map = {
                QuestionDifficulty.EXPERT: QuestionDifficulty.HARD,
                QuestionDifficulty.HARD: QuestionDifficulty.MEDIUM,
                QuestionDifficulty.MEDIUM: QuestionDifficulty.EASY,
                QuestionDifficulty.EASY: QuestionDifficulty.EASY,
            }
            base_difficulty = difficulty_map.get(base_difficulty, base_difficulty)
        
        return base_difficulty

    def generate_question(
        self,
        target_unit: str,
        difficulty: QuestionDifficulty,
        unit_definition: dict,
    ) -> AdaptiveQuestion:
        """Generate a personalized question for a specific knowledge unit."""
        
        # Select template
        templates = self.templates.get(difficulty, self.templates[QuestionDifficulty.MEDIUM])
        template = random.choice(templates)
        
        # Generate question text from template
        question_text = self._fill_template(template["template"], unit_definition, difficulty)
        
        # Generate hints based on difficulty
        hints = self._generate_hints(unit_definition, difficulty)
        
        # Generate expected answer elements
        expected_elements = self._generate_expected_elements(unit_definition)
        
        # Generate misconception traps
        misconception_traps = self._generate_misconception_traps(unit_definition)
        
        return AdaptiveQuestion(
            question_id=f"adaptive_{target_unit}_{random.randint(1000, 9999)}",
            question_text=question_text,
            target_knowledge_unit=target_unit,
            difficulty=difficulty,
            question_type=template["type"],
            estimated_time_minutes=template["time"],
            hints=hints,
            expected_answer_elements=expected_elements,
            misconception_traps=misconception_traps,
        )

    def _fill_template(
        self,
        template: str,
        unit_definition: dict,
        difficulty: QuestionDifficulty,
    ) -> str:
        """Fill in template variables with unit-specific content."""
        unit_name = unit_definition.get("name", unit_definition.get("id", "concept"))
        
        # Simple template filling - in production would be more sophisticated
        filled = template.replace("{concept}", unit_name)
        
        # Add difficulty-specific content
        if difficulty == QuestionDifficulty.EASY:
            filled = filled.replace("{code}", f"x = 5\nprint(x)")
        elif difficulty == QuestionDifficulty.MEDIUM:
            filled = filled.replace("{requirement}", f"demonstrates understanding of {unit_name}")
        
        return filled

    def _generate_hints(
        self,
        unit_definition: dict,
        difficulty: QuestionDifficulty,
    ) -> list[str]:
        """Generate progressive hints."""
        hints = []
        
        if difficulty.value >= QuestionDifficulty.MEDIUM.value:
            hints.append(f"Think about the key principles of {unit_definition.get('name', 'this concept')}")
        
        if difficulty.value >= QuestionDifficulty.HARD.value:
            hints.append("Consider edge cases and boundary conditions")
        
        return hints

    def _generate_expected_elements(
        self,
        unit_definition: dict,
    ) -> list[str]:
        """Generate expected elements in correct answer."""
        return [
            unit_definition.get("name", "concept"),
            "correct syntax",
            "logical reasoning",
        ]

    def _generate_misconception_traps(
        self,
        unit_definition: dict,
    ) -> list[str]:
        """Generate common wrong answers to watch for."""
        return [
            f"confusing {unit_definition.get('name', 'concept')} with similar concepts",
            "syntax errors",
            "logical fallacies",
        ]

    def generate_adaptive_test(
        self,
        knowledge_state: dict,
        learned_units: set,
        unit_definitions: list[dict],
        test_history: list[dict],
        misconceptions: list[str],
        num_questions: int = 5,
    ) -> dict:
        """
        Generate a complete adaptive test.
        
        This is the main entry point for adaptive test generation.
        """
        # Identify knowledge gaps
        gaps = self.identify_knowledge_gaps(
            knowledge_state=knowledge_state,
            learned_units=learned_units,
            test_history=test_history,
            misconceptions=misconceptions,
        )
        
        # Generate questions for top gaps
        questions = []
        used_units = set()
        
        for gap in gaps[:num_questions]:
            if gap.unit_id in used_units:
                continue
            
            # Find unit definition
            unit_def = next(
                (u for u in unit_definitions if u["id"] == gap.unit_id),
                None
            )
            if not unit_def:
                continue
            
            # Generate question
            question = self.generate_question(
                target_unit=gap.unit_id,
                difficulty=gap.recommended_difficulty,
                unit_definition=unit_def,
            )
            
            questions.append(question)
            used_units.add(gap.unit_id)
        
        # If not enough questions, fill with random learned concepts
        if len(questions) < num_questions:
            remaining_learned = learned_units - used_units
            for unit_id in list(remaining_learned)[:num_questions - len(questions)]:
                unit_def = next(
                    (u for u in unit_definitions if u["id"] == unit_id),
                    None
                )
                if unit_def:
                    p_know = knowledge_state.get(unit_id, {}).get("p_know", 0.5)
                    difficulty = self.select_difficulty(p_know, "reinforcement", 0)
                    
                    question = self.generate_question(
                        target_unit=unit_id,
                        difficulty=difficulty,
                        unit_definition=unit_def,
                    )
                    questions.append(question)
        
        # Calculate test metrics
        total_time = sum(q.estimated_time_minutes for q in questions)
        avg_difficulty = sum(q.difficulty.value for q in questions) / max(1, len(questions))
        
        return {
            "test_id": f"adaptive_test_{random.randint(10000, 99999)}",
            "generated_at": "now",
            "questions": [
                {
                    "id": q.question_id,
                    "text": q.question_text,
                    "target_unit": q.target_knowledge_unit,
                    "difficulty": q.difficulty.name,
                    "type": q.question_type,
                    "estimated_time": q.estimated_time_minutes,
                    "hints": q.hints,
                }
                for q in questions
            ],
            "test_metadata": {
                "total_questions": len(questions),
                "total_estimated_time": total_time,
                "average_difficulty": round(avg_difficulty, 2),
                "knowledge_gaps_targeted": [g.unit_id for g in gaps[:len(questions)]],
                "adaptive_strategy": "BKT-based gap identification with IRT difficulty selection",
            },
        }


def generate_adaptive_test_for_ta(
    ta,
    num_questions: int = 5,
) -> dict:
    """
    Generate an adaptive test for a specific TA instance.
    
    This is the API-facing function.
    """
    from src.api.domain_helpers import get_tracker_for_ta, get_domain_adapter
    
    # Get tracker and state
    tracker = get_tracker_for_ta(ta)
    knowledge_state = tracker.get_full_state().get("units", {})
    learned_units = set(tracker.get_learned_units())
    
    # Get unit definitions
    adapter = get_domain_adapter(ta.domain_id)
    unit_definitions = adapter.load_knowledge_units()
    
    # Get misconceptions
    active_misconceptions = tracker.get_active_misconception_ids()
    
    # Create generator
    generator = AdaptiveTestGenerator(domain=ta.domain_id)
    
    # Generate test
    return generator.generate_adaptive_test(
        knowledge_state=knowledge_state,
        learned_units=learned_units,
        unit_definitions=unit_definitions,
        test_history=[],  # Would be fetched from DB in production
        misconceptions=active_misconceptions,
        num_questions=num_questions,
    )
