"""
Teaching Interpreter: map student natural language input to knowledge units (NLP -> KU).
LLM Call #1 in the cycle. Returns structured {topic_taught, knowledge_units_taught, quality_score}.
"""

import json
import re

from src.llm.client import llm_completion


def interpret_teaching(
    student_input: str,
    all_unit_ids: list[str],
    *,
    filled_prompt: str | None = None,
    use_llm: bool | None = None,
) -> dict:
    """
    Parse student teaching input into structured teaching event data.
    - student_input: raw text from the student.
    - all_unit_ids: list of valid KU ids for the domain (to validate LLM output).
    - filled_prompt: prompt for the LLM (from domain adapter).
    - use_llm: if True and filled_prompt, call LLM; else return heuristic/safe default.

    Returns dict with: topic_taught (str), knowledge_units_taught (list[str]), quality_score (float 0-1).
    """
    valid_ids = set(all_unit_ids)

    if use_llm is False or not filled_prompt:
        return _heuristic_interpret(student_input, valid_ids)

    if use_llm is None or use_llm is True:
        out = llm_completion(filled_prompt, max_tokens=200, temperature=0.2)
        if out:
            parsed = _parse_llm_interpretation(out, valid_ids)
            if parsed:
                return parsed
    return _heuristic_interpret(student_input, valid_ids)


def _parse_llm_interpretation(raw: str, valid_ids: set[str]) -> dict | None:
    """Try to extract topic, list of unit ids, and quality from LLM output."""
    raw = (raw or "").strip()
    # Try JSON block first
    json_match = re.search(r"\{[^{}]*\"knowledge_units_taught\"[^{}]*\}", raw, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            units = data.get("knowledge_units_taught", [])
            if isinstance(units, list):
                units = [u for u in units if isinstance(u, str) and u in valid_ids]
            else:
                units = []
            topic = data.get("topic_taught", "")
            if not isinstance(topic, str):
                topic = str(topic)
            quality = data.get("quality_score", 0.7)
            if isinstance(quality, (int, float)) and 0 <= quality <= 1:
                pass
            else:
                quality = 0.7
            return {
                "topic_taught": topic or "Teaching",
                "knowledge_units_taught": units[:20],
                "quality_score": float(quality),
            }
        except json.JSONDecodeError:
            pass
    # Try line-based: "topic_taught: ..." and "knowledge_units_taught: id1, id2"
    topic = ""
    units = []
    for line in raw.split("\n"):
        line = line.strip()
        if line.lower().startswith("topic"):
            topic = line.split(":", 1)[-1].strip()
        if line.lower().startswith("knowledge_units") or line.lower().startswith("units"):
            part = line.split(":", 1)[-1].strip()
            for u in re.split(r"[\s,]+", part):
                u = u.strip().strip("[]\"'")
                if u in valid_ids:
                    units.append(u)
    if units or topic:
        return {
            "topic_taught": topic or "Teaching",
            "knowledge_units_taught": units[:20],
            "quality_score": 0.7,
        }
    return None


def _heuristic_interpret(student_input: str, valid_ids: set[str]) -> dict:
    """Simple keyword heuristic when LLM is not used or fails."""
    text = (student_input or "").lower()
    units = []
    if "variable" in text or "assign" in text or "=" in text:
        if "variable_assignment" in valid_ids:
            units.append("variable_assignment")
    if "print" in text:
        if "print_function" in valid_ids:
            units.append("print_function")
    if "input" in text:
        if "user_input" in valid_ids:
            units.append("user_input")
    if "loop" in text or "for " in text or "while" in text:
        if "for_loop_range" in valid_ids:
            units.append("for_loop_range")
        if "while_loop" in valid_ids and "while" in text:
            units.append("while_loop")
    if "if " in text or "condition" in text or "else" in text:
        if "if_statement" in valid_ids:
            units.append("if_statement")
        if "if_else" in valid_ids:
            units.append("if_else")
    if "list" in text or "[]" in text:
        if "list_creation" in valid_ids:
            units.append("list_creation")
        if "list_indexing" in valid_ids:
            units.append("list_indexing")
    if "number" in text or "int" in text or "float" in text:
        if "data_types_int_float" in valid_ids:
            units.append("data_types_int_float")
    if "string" in text or "str" in text:
        if "data_types_string" in valid_ids:
            units.append("data_types_string")
    if "operator" in text or "+" in text or "-" in text:
        if "arithmetic_operators" in valid_ids:
            units.append("arithmetic_operators")
    if not units and valid_ids:
        # Default: at least one unit so we don't drop the teaching
        units = [next(iter(valid_ids))]
    return {
        "topic_taught": (student_input or "Teaching")[:200],
        "knowledge_units_taught": units[:20],
        "quality_score": 0.6 if units else 0.3,
    }
