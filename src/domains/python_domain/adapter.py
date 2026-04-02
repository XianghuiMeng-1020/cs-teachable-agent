"""Python domain adapter: knowledge units, problems, misconceptions, prompts, evaluation."""

import json
from pathlib import Path

from src.domains.base import DomainAdapter


def _default_seed_dir() -> Path:
    # Repo root: src/domains/python_domain/adapter.py -> ../../.. = repo root
    return Path(__file__).resolve().parent.parent.parent.parent / "seed"


def _default_prompts_dir() -> Path:
    return Path(__file__).resolve().parent / "prompts"


class PythonDomainAdapter(DomainAdapter):
    domain_id = "python"

    def __init__(
        self,
        seed_dir: Path | None = None,
        prompts_dir: Path | None = None,
    ):
        self._seed_dir = seed_dir or _default_seed_dir()
        self._prompts_dir = prompts_dir or _default_prompts_dir()
        self._knowledge_units: list[dict] | None = None
        self._problems: list[dict] | None = None
        self._misconceptions: list[dict] | None = None

    def load_knowledge_units(self) -> list[dict]:
        if self._knowledge_units is not None:
            return self._knowledge_units
        path = self._seed_dir / "knowledge_units.json"
        if not path.exists():
            path = self._seed_dir / "knowledge-units-stage1.json"
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self._knowledge_units = data.get("knowledge_units", [])
        return self._knowledge_units

    def load_problems(self) -> list[dict]:
        if self._problems is not None:
            return self._problems
        all_problems: list[dict] = []
        seen_ids: set[str] = set()
        # Load main problems
        path = self._seed_dir / "problems.json"
        if not path.exists():
            path = self._seed_dir / "sample-problems-stage1.json"
        if path.exists():
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for p in data.get("problems", []):
                pid = p.get("problem_id")
                if pid and pid not in seen_ids:
                    all_problems.append(p)
                    seen_ids.add(pid)
        # Load expanded teach problems
        expanded_path = self._seed_dir / "problems-teach-expanded.json"
        if expanded_path.exists():
            with open(expanded_path, encoding="utf-8") as f:
                data = json.load(f)
            for p in data.get("problems", []):
                pid = p.get("problem_id")
                if pid and pid not in seen_ids:
                    all_problems.append(p)
                    seen_ids.add(pid)
        self._problems = all_problems
        return self._problems

    def load_misconceptions(self) -> list[dict]:
        if self._misconceptions is not None:
            return self._misconceptions
        path = self._seed_dir / "misconceptions.json"
        if not path.exists():
            path = self._seed_dir / "misconceptions-stage1.json"
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self._misconceptions = data.get("misconceptions", [])
        return self._misconceptions

    def evaluate_attempt(self, problem: dict, code_or_answer: str) -> dict:
        """Execute Python code and compare stdout to expected output."""
        from src.core.evaluator import evaluate_attempt as eval_attempt
        return eval_attempt(problem, code_or_answer)

    def _load_template(self, name: str) -> str:
        path = self._prompts_dir / f"{name}.md"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def get_code_generation_prompt(
        self,
        knowledge_state: dict,
        problem: dict,
        active_misconceptions: list[str],
    ) -> str:
        template = self._load_template("code_generation")
        if not template:
            return ""
        units = []
        if isinstance(knowledge_state, dict) and "units" in knowledge_state:
            units = [
                uid for uid, rec in knowledge_state["units"].items()
                if rec.get("status") in ("learned", "partially_learned")
            ]
        units_str = ", ".join(sorted(units))
        mis_str = ", ".join(active_misconceptions) if active_misconceptions else "None"
        return (
            template.replace("{{PROBLEM_ID}}", problem.get("problem_id", ""))
            .replace("{{PROBLEM_STATEMENT}}", problem.get("problem_statement", ""))
            .replace("{{INPUT_SPEC}}", str(problem.get("input_spec") or "No input."))
            .replace("{{LEARNED_UNITS}}", units_str)
            .replace("{{ACTIVE_MISCONCEPTIONS}}", mis_str)
        )

    def get_conversation_prompt(
        self,
        knowledge_state: dict,
        teaching_input: dict,
        learned_units: list[str],
    ) -> str:
        template = self._load_template("conversation")
        if not template:
            return ""
        topic = teaching_input.get("topic_taught", "")
        note = teaching_input.get("note", "")
        mis_ids = []
        if isinstance(knowledge_state, dict) and "units" in knowledge_state:
            for rec in knowledge_state["units"].values():
                for m in rec.get("active_misconceptions", []):
                    mid = m.get("misconception_id")
                    if mid:
                        mis_ids.append(mid)
        mis_str = ", ".join(mis_ids) if mis_ids else "None"
        units_str = ", ".join(sorted(learned_units))
        return (
            template.replace("{{LEARNED_UNITS}}", units_str)
            .replace("{{TEACHING_TOPIC}}", topic)
            .replace("{{TEACHING_NOTE}}", note)
            .replace("{{ACTIVE_MISCONCEPTIONS}}", mis_str)
        )

    def get_teaching_interpreter_prompt(self, student_input: str) -> str:
        template = self._load_template("teaching_interpreter")
        if not template:
            return ""
        units = self.load_knowledge_units()
        unit_ids = [u["id"] for u in units]
        units_list = ", ".join(unit_ids)
        return template.replace("{{STUDENT_INPUT}}", student_input).replace(
            "{{KNOWN_UNIT_IDS}}", units_list
        )
