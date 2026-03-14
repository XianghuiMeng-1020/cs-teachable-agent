"""Domain adapter abstract base class. All domains implement this interface."""

from abc import ABC, abstractmethod


class DomainAdapter(ABC):
    """All domains (Python, Database, AI Literacy) implement this interface."""

    domain_id: str  # "python", "database", "ai_literacy"

    @abstractmethod
    def load_knowledge_units(self) -> list[dict]:
        """Load all knowledge units for this domain from seed data."""
        ...

    @abstractmethod
    def load_problems(self) -> list[dict]:
        """Load problem bank for this domain."""
        ...

    @abstractmethod
    def load_misconceptions(self) -> list[dict]:
        """Load misconception catalog for this domain."""
        ...

    @abstractmethod
    def evaluate_attempt(self, problem: dict, code_or_answer: str) -> dict:
        """
        Evaluate TA's attempt.
        Returns: {passed: bool, details: [...], score: float}
        """
        ...

    @abstractmethod
    def get_code_generation_prompt(
        self,
        knowledge_state: dict,
        problem: dict,
        active_misconceptions: list[str],
    ) -> str:
        """Build LLM prompt for TA code/answer generation, constrained by state."""
        ...

    @abstractmethod
    def get_conversation_prompt(
        self,
        knowledge_state: dict,
        teaching_input: dict,
        learned_units: list[str],
    ) -> str:
        """Build LLM prompt for TA learner-style response."""
        ...

    @abstractmethod
    def get_teaching_interpreter_prompt(self, student_input: str) -> str:
        """Build LLM prompt to extract knowledge units from student's teaching."""
        ...
