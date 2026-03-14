"""Database domain adapter: SQL problems, execute and compare result sets. Paper 2 extension."""

from pathlib import Path

from src.domains.base import DomainAdapter


class DatabaseDomainAdapter(DomainAdapter):
    domain_id = "database"

    def __init__(self, seed_dir: Path | None = None):
        self._seed_dir = seed_dir or Path(__file__).resolve().parent / "seed"
        self._knowledge_units: list[dict] | None = None
        self._problems: list[dict] | None = None
        self._misconceptions: list[dict] | None = None

    def load_knowledge_units(self) -> list[dict]:
        if self._knowledge_units is not None:
            return self._knowledge_units
        path = self._seed_dir / "knowledge_units.json"
        if not path.exists():
            self._knowledge_units = []
            return self._knowledge_units
        import json
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self._knowledge_units = data.get("knowledge_units", [])
        return self._knowledge_units

    def load_problems(self) -> list[dict]:
        if self._problems is not None:
            return self._problems
        path = self._seed_dir / "problems.json"
        if not path.exists():
            self._problems = []
            return self._problems
        import json
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self._problems = data.get("problems", [])
        return self._problems

    def load_misconceptions(self) -> list[dict]:
        if self._misconceptions is not None:
            return self._misconceptions
        path = self._seed_dir / "misconceptions.json"
        if not path.exists():
            self._misconceptions = []
            return self._misconceptions
        import json
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self._misconceptions = data.get("misconceptions", [])
        return self._misconceptions

    def evaluate_attempt(self, problem: dict, code_or_answer: str) -> dict:
        """Execute SQL against test DB and compare result set. Stub: not implemented."""
        return {"passed": False, "details": [], "score": 0.0}

    def get_code_generation_prompt(
        self,
        knowledge_state: dict,
        problem: dict,
        active_misconceptions: list[str],
    ) -> str:
        return ""

    def get_conversation_prompt(
        self,
        knowledge_state: dict,
        teaching_input: dict,
        learned_units: list[str],
    ) -> str:
        return ""

    def get_teaching_interpreter_prompt(self, student_input: str) -> str:
        return ""
