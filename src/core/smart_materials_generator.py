"""
Smart Learning Materials Generator

Automatically generates personalized learning materials based on:
- Student's weak areas
- Learning style preferences
- Current knowledge state
- Difficulty progression

Research Applications:
- Adaptive content generation
- Personalized learning resources
- Scaffolding and fading support
- Multi-modal material creation
"""

import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class MaterialType(Enum):
    """Types of learning materials."""
    EXPLANATION = "explanation"
    EXAMPLE = "example"
    PRACTICE_PROBLEM = "practice_problem"
    QUIZ = "quiz"
    CODE_WALKTHROUGH = "code_walkthrough"
    VISUALIZATION = "visualization"
    CHEAT_SHEET = "cheat_sheet"
    COMPARISON = "comparison"


class DifficultyLevel(Enum):
    SCAFFOLDED = "scaffolded"  # With hints and support
    GUIDED = "guided"  # Some guidance
    INDEPENDENT = "independent"  # No support
    CHALLENGE = "challenge"  # Above current level


@dataclass
class WeakArea:
    """Identified weak area for targeting."""
    concept_id: str
    concept_name: str
    mastery_level: float
    misconception_patterns: List[str]
    attempts_count: int
    failure_rate: float


@dataclass
class LearningMaterial:
    """Generated learning material."""
    material_id: str
    material_type: MaterialType
    difficulty: DifficultyLevel
    target_concept: str
    title: str
    content: str
    hints: List[str]
    estimated_time: int  # minutes
    prerequisites: List[str]
    follow_up: List[str]
    format: str  # "text", "code", "interactive"


@dataclass
class MaterialSequence:
    """A sequence of materials for learning a concept."""
    sequence_id: str
    target_concept: str
    materials: List[LearningMaterial]
    total_estimated_time: int
    learning_objectives: List[str]
    success_criteria: str


class SmartMaterialsGenerator:
    """Generates personalized learning materials."""
    
    # Templates for different material types
    TEMPLATES = {
        "python": {
            MaterialType.EXPLANATION: [
                "Let's understand {concept} through simple analogies...",
                "The key idea behind {concept} is...",
                "Think of {concept} like this...",
            ],
            MaterialType.EXAMPLE: [
                "Here's how {concept} works in practice:\n\n```python\n{code}\n```",
                "Let's see {concept} in action:\n\n```python\n{code}\n```",
            ],
            MaterialType.PRACTICE_PROBLEM: [
                "Now it's your turn! Try this:\n\n{problem}\n\nHint: {hint}",
                "Practice makes perfect. Solve this:\n\n{problem}",
            ],
            MaterialType.CODE_WALKTHROUGH: [
                "Let's walk through this code step by step:\n\n```python\n{code}\n```\n\n1. First, we...\n2. Then...\n3. Finally...",
            ],
            MaterialType.CHEAT_SHEET: [
                "Quick Reference: {concept}\n\n• Key syntax: {syntax}\n• Common uses: {uses}\n• Remember: {tips}",
            ],
        },
    }
    
    def __init__(self, domain: str = "python"):
        self.domain = domain
        self.templates = self.TEMPLATES.get(domain, self.TEMPLATES["python"])
    
    def identify_weak_areas(
        self,
        knowledge_state: Dict[str, float],
        test_history: List[Dict],
        misconception_data: List[Dict],
    ) -> List[WeakArea]:
        """
        Identify weak areas based on performance data.
        
        Returns prioritized list of weak areas.
        """
        weak_areas = []
        
        for concept_id, mastery in knowledge_state.items():
            # Skip well-mastered concepts
            if mastery > 0.8:
                continue
            
            # Get test history for this concept
            concept_tests = [
                t for t in test_history
                if concept_id in t.get("concepts_tested", [])
            ]
            
            if not concept_tests:
                # Untested concept - might be new
                weak_areas.append(WeakArea(
                    concept_id=concept_id,
                    concept_name=concept_id.replace("_", " ").title(),
                    mastery_level=mastery,
                    misconception_patterns=[],
                    attempts_count=0,
                    failure_rate=0.0,
                ))
                continue
            
            # Calculate failure rate
            passed = sum(1 for t in concept_tests if t.get("passed", False))
            failure_rate = 1 - (passed / len(concept_tests))
            
            # Get misconceptions
            patterns = []
            for m in misconception_data:
                if m.get("concept_id") == concept_id:
                    patterns.extend(m.get("patterns", []))
            
            # Determine if this is a weak area
            is_weak = (
                mastery < 0.5 or
                failure_rate > 0.5 or
                len(patterns) > 0
            )
            
            if is_weak:
                weak_areas.append(WeakArea(
                    concept_id=concept_id,
                    concept_name=concept_id.replace("_", " ").title(),
                    mastery_level=mastery,
                    misconception_patterns=list(set(patterns)),
                    attempts_count=len(concept_tests),
                    failure_rate=failure_rate,
                ))
        
        # Sort by priority (lower mastery + higher failure rate = higher priority)
        weak_areas.sort(
            key=lambda w: (1 - w.mastery_level) * 0.6 + w.failure_rate * 0.4,
            reverse=True
        )
        
        return weak_areas
    
    def generate_for_weak_area(
        self,
        weak_area: WeakArea,
        learning_style: str = "balanced",  # "visual", "practical", "theoretical", "balanced"
    ) -> MaterialSequence:
        """
        Generate a sequence of materials for a weak area.
        
        Args:
            weak_area: The weak area to target
            learning_style: Preferred learning style
        
        Returns:
            MaterialSequence with scaffolded materials
        """
        materials = []
        
        # Determine difficulty progression based on mastery
        if weak_area.mastery_level < 0.3:
            difficulty_sequence = [
                DifficultyLevel.SCAFFOLDED,
                DifficultyLevel.SCAFFOLDED,
                DifficultyLevel.GUIDED,
            ]
        elif weak_area.mastery_level < 0.6:
            difficulty_sequence = [
                DifficultyLevel.GUIDED,
                DifficultyLevel.GUIDED,
                DifficultyLevel.INDEPENDENT,
            ]
        else:
            difficulty_sequence = [
                DifficultyLevel.INDEPENDENT,
                DifficultyLevel.CHALLENGE,
            ]
        
        # Generate materials
        for i, difficulty in enumerate(difficulty_sequence):
            if i == 0:
                # Always start with explanation
                material = self._generate_explanation(weak_area, difficulty)
            elif i == 1:
                # Follow with example
                material = self._generate_example(weak_area, difficulty)
            elif learning_style == "practical":
                material = self._generate_practice_problem(weak_area, difficulty)
            else:
                material = self._generate_quiz(weak_area, difficulty)
            
            materials.append(material)
        
        # Add cheat sheet at the end
        materials.append(self._generate_cheat_sheet(weak_area))
        
        total_time = sum(m.estimated_time for m in materials)
        
        return MaterialSequence(
            sequence_id=f"seq_{weak_area.concept_id}_{random.randint(1000, 9999)}",
            target_concept=weak_area.concept_id,
            materials=materials,
            total_estimated_time=total_time,
            learning_objectives=[
                f"Understand the concept of {weak_area.concept_name}",
                f"Apply {weak_area.concept_name} in practical scenarios",
                f"Avoid common misconceptions about {weak_area.concept_name}",
            ],
            success_criteria=f"Achieve 80% mastery on {weak_area.concept_name}",
        )
    
    def _generate_explanation(
        self,
        weak_area: WeakArea,
        difficulty: DifficultyLevel,
    ) -> LearningMaterial:
        """Generate explanation material."""
        template = random.choice(self.templates[MaterialType.EXPLANATION])
        
        content = template.format(
            concept=weak_area.concept_name,
        )
        
        # Add scaffolding based on difficulty
        hints = []
        if difficulty == DifficultyLevel.SCAFFOLDED:
            hints.append("Take your time with each step")
            hints.append("Read the explanation twice if needed")
        
        return LearningMaterial(
            material_id=f"expl_{weak_area.concept_id}_{random.randint(100, 999)}",
            material_type=MaterialType.EXPLANATION,
            difficulty=difficulty,
            target_concept=weak_area.concept_id,
            title=f"Understanding {weak_area.concept_name}",
            content=content,
            hints=hints,
            estimated_time=5,
            prerequisites=[],
            follow_up=["example", "practice"],
            format="text",
        )
    
    def _generate_example(
        self,
        weak_area: WeakArea,
        difficulty: DifficultyLevel,
    ) -> LearningMaterial:
        """Generate example material."""
        template = random.choice(self.templates[MaterialType.EXAMPLE])
        
        # Generate simple example code
        example_code = self._generate_example_code(weak_area.concept_id)
        
        content = template.format(
            concept=weak_area.concept_name,
            code=example_code,
        )
        
        hints = []
        if difficulty == DifficultyLevel.SCAFFOLDED:
            hints.append("The key line is highlighted")
        
        return LearningMaterial(
            material_id=f"ex_{weak_area.concept_id}_{random.randint(100, 999)}",
            material_type=MaterialType.EXAMPLE,
            difficulty=difficulty,
            target_concept=weak_area.concept_id,
            title=f"Example: {weak_area.concept_name} in Action",
            content=content,
            hints=hints,
            estimated_time=8,
            prerequisites=[weak_area.concept_id],
            follow_up=["practice"],
            format="code",
        )
    
    def _generate_practice_problem(
        self,
        weak_area: WeakArea,
        difficulty: DifficultyLevel,
    ) -> LearningMaterial:
        """Generate practice problem."""
        template = random.choice(self.templates[MaterialType.PRACTICE_PROBLEM])
        
        # Generate problem based on concept
        problem, hint = self._generate_problem(weak_area)
        
        content = template.format(
            problem=problem,
            hint=hint if difficulty != DifficultyLevel.INDEPENDENT else "",
        )
        
        hints = []
        if difficulty == DifficultyLevel.SCAFFOLDED:
            hints.append(hint)
            hints.append("Start with the basics")
        elif difficulty == DifficultyLevel.GUIDED:
            hints.append(hint)
        
        return LearningMaterial(
            material_id=f"prac_{weak_area.concept_id}_{random.randint(100, 999)}",
            material_type=MaterialType.PRACTICE_PROBLEM,
            difficulty=difficulty,
            target_concept=weak_area.concept_id,
            title=f"Practice: {weak_area.concept_name}",
            content=content,
            hints=hints,
            estimated_time=10,
            prerequisites=[weak_area.concept_id],
            follow_up=["quiz"],
            format="interactive",
        )
    
    def _generate_quiz(
        self,
        weak_area: WeakArea,
        difficulty: DifficultyLevel,
    ) -> LearningMaterial:
        """Generate quiz questions."""
        questions = self._generate_quiz_questions(weak_area, num_questions=3)
        
        content = f"Quick Check: {weak_area.concept_name}\n\n"
        for i, q in enumerate(questions, 1):
            content += f"{i}. {q['question']}\n"
            for opt in q['options']:
                content += f"   {opt}\n"
            content += "\n"
        
        return LearningMaterial(
            material_id=f"quiz_{weak_area.concept_id}_{random.randint(100, 999)}",
            material_type=MaterialType.QUIZ,
            difficulty=difficulty,
            target_concept=weak_area.concept_id,
            title=f"Quick Check: {weak_area.concept_name}",
            content=content,
            hints=["Read each question carefully"],
            estimated_time=5,
            prerequisites=[weak_area.concept_id],
            follow_up=[],
            format="interactive",
        )
    
    def _generate_cheat_sheet(
        self,
        weak_area: WeakArea,
    ) -> LearningMaterial:
        """Generate quick reference."""
        template = random.choice(self.templates[MaterialType.CHEAT_SHEET])
        
        content = template.format(
            concept=weak_area.concept_name,
            syntax=self._get_syntax_summary(weak_area.concept_id),
            uses=self._get_common_uses(weak_area.concept_id),
            tips=self._get_pro_tips(weak_area.concept_id, weak_area.misconception_patterns),
        )
        
        return LearningMaterial(
            material_id=f"cheat_{weak_area.concept_id}_{random.randint(100, 999)}",
            material_type=MaterialType.CHEAT_SHEET,
            difficulty=DifficultyLevel.INDEPENDENT,
            target_concept=weak_area.concept_id,
            title=f"Quick Reference: {weak_area.concept_name}",
            content=content,
            hints=["Bookmark this for quick reference"],
            estimated_time=2,
            prerequisites=[],
            follow_up=[],
            format="text",
        )
    
    def _generate_example_code(self, concept_id: str) -> str:
        """Generate example code for a concept."""
        examples = {
            "variable_assignment": "x = 5\nprint(f\"The value is: {x}\")",
            "for_loop": "for i in range(3):\n    print(f\"Iteration: {i}\")",
            "if_statement": "age = 18\nif age >= 18:\n    print(\"Adult\")\nelse:\n    print(\"Minor\")",
            "function_definition": "def greet(name):\n    return f\"Hello, {name}!\"\n\nresult = greet(\"Alice\")",
        }
        
        return examples.get(concept_id, f"# Example code for {concept_id}\nprint('Hello World')")
    
    def _generate_problem(self, weak_area: WeakArea) -> tuple:
        """Generate practice problem and hint."""
        problems = {
            "variable_assignment": (
                "Create a variable called 'score' with value 100, then print it.",
                "Use the assignment operator (=) to create the variable."
            ),
            "for_loop": (
                "Write a for loop that prints numbers 1 through 5.",
                "Use range() to generate the sequence."
            ),
            "if_statement": (
                "Write code that checks if a number is positive and prints a message.",
                "Use the > operator to check if greater than 0."
            ),
        }
        
        return problems.get(
            weak_area.concept_id,
            (f"Practice using {weak_area.concept_name}", "Start with a simple example.")
        )
    
    def _generate_quiz_questions(self, weak_area: WeakArea, num_questions: int = 3) -> List[Dict]:
        """Generate quiz questions."""
        questions = []
        
        # Question 1: Concept understanding
        questions.append({
            "question": f"What is the primary purpose of {weak_area.concept_name}?",
            "options": [
                "a) To store data temporarily",
                "b) To control program flow",
                "c) To repeat operations",
                "d) To define functions",
            ],
            "correct": "a",
        })
        
        # Question 2: Syntax recognition
        questions.append({
            "question": f"Which of the following shows correct {weak_area.concept_name} syntax?",
            "options": [
                f"a) {weak_area.concept_id} = value",
                f"b) value = {weak_area.concept_id}",
                f"c) {weak_area.concept_id}(value)",
                f"d) #{weak_area.concept_id}",
            ],
            "correct": "a",
        })
        
        # Question 3: Application
        questions.append({
            "question": f"When would you use {weak_area.concept_name} in a program?",
            "options": [
                "a) When you need to save a value for later use",
                "b) When you want to stop the program",
                "c) When you need to connect to the internet",
                "d) When you want to delete files",
            ],
            "correct": "a",
        })
        
        return questions[:num_questions]
    
    def _get_syntax_summary(self, concept_id: str) -> str:
        """Get syntax summary for cheat sheet."""
        syntax = {
            "variable_assignment": "variable_name = value",
            "for_loop": "for item in sequence:",
            "if_statement": "if condition:",
        }
        return syntax.get(concept_id, f"{concept_id}(args)")
    
    def _get_common_uses(self, concept_id: str) -> str:
        """Get common uses for cheat sheet."""
        uses = {
            "variable_assignment": "Storing user input, calculation results, configuration values",
            "for_loop": "Iterating through lists, processing each item, repeating actions",
            "if_statement": "Making decisions, validation, branching logic",
        }
        return uses.get(concept_id, "Various programming tasks")
    
    def _get_pro_tips(self, concept_id: str, misconceptions: List[str]) -> str:
        """Get pro tips for cheat sheet."""
        tips = ["Practice regularly to build muscle memory"]
        
        if misconceptions:
            tips.append(f"Watch out for: {misconceptions[0]}")
        
        return "; ".join(tips)
    
    def generate_daily_practice_set(
        self,
        weak_areas: List[WeakArea],
        max_time: int = 20,
    ) -> List[LearningMaterial]:
        """
        Generate a daily practice set targeting multiple weak areas.
        
        Args:
            weak_areas: List of weak areas
            max_time: Maximum time in minutes
        
        Returns:
            List of materials fitting within time budget
        """
        practice_set = []
        remaining_time = max_time
        
        # Sort by priority
        weak_areas.sort(key=lambda w: w.mastery_level)
        
        for weak_area in weak_areas[:3]:  # Top 3 weak areas
            if remaining_time <= 0:
                break
            
            # Generate quick practice
            problem = self._generate_practice_problem(
                weak_area,
                DifficultyLevel.GUIDED
            )
            
            if problem.estimated_time <= remaining_time:
                practice_set.append(problem)
                remaining_time -= problem.estimated_time
        
        return practice_set


def generate_personalized_materials(
    knowledge_state: Dict[str, float],
    test_history: List[Dict],
    learning_style: str = "balanced",
) -> List[MaterialSequence]:
    """
    Main API-facing function to generate personalized materials.
    
    Args:
        knowledge_state: Current knowledge state
        test_history: Past test results
        learning_style: Preferred learning style
    
    Returns:
        List of material sequences for weak areas
    """
    generator = SmartMaterialsGenerator()
    
    # Identify weak areas
    weak_areas = generator.identify_weak_areas(
        knowledge_state=knowledge_state,
        test_history=test_history,
        misconception_data=[],
    )
    
    # Generate sequences for top weak areas
    sequences = []
    for weak_area in weak_areas[:3]:  # Limit to top 3
        sequence = generator.generate_for_weak_area(weak_area, learning_style)
        sequences.append(sequence)
    
    return sequences
