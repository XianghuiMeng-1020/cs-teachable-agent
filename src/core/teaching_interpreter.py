"""
Teaching Interpreter: map student natural language input to knowledge units (NLP -> KU).
Returns structured teaching event with multidimensional quality (accuracy, completeness, clarity,
misconception_correction) and interpretation_class (correct/incorrect/ambiguous).
"""

import json
import re
from typing import Any

from src.llm.client import llm_completion

INTERPRETATION_CORRECT = "correct"
INTERPRETATION_INCORRECT = "incorrect"
INTERPRETATION_AMBIGUOUS = "ambiguous"


def _default_quality() -> dict[str, Any]:
    return {
        "quality_score": 0.6,
        "quality_accuracy": 0.6,
        "quality_completeness": 0.5,
        "quality_clarity": 0.6,
        "misconception_correction": False,
        "interpretation_class": INTERPRETATION_AMBIGUOUS,
    }


def interpret_teaching(
    student_input: str,
    all_unit_ids: list[str],
    *,
    filled_prompt: str | None = None,
    use_llm: bool | None = None,
    conversation_history: list[dict] | None = None,
) -> dict:
    """
    Parse student teaching input into structured teaching event data.
    - student_input: raw text from the student.
    - all_unit_ids: list of valid KU ids for the domain (to validate LLM output).
    - filled_prompt: prompt for the LLM (from domain adapter).
    - use_llm: if True and filled_prompt, call LLM; else return heuristic/safe default.
    - conversation_history: optional list of {role, content} for multi-turn context.

    Returns dict with: topic_taught, knowledge_units_taught, quality_score, quality_accuracy,
    quality_completeness, quality_clarity, misconception_correction, interpretation_class.
    """
    valid_ids = set(all_unit_ids)
    default_q = _default_quality()

    if use_llm is False or not filled_prompt:
        out = _heuristic_interpret(student_input, valid_ids)
        return {**default_q, **out}

    if use_llm is None or use_llm is True:
        out = llm_completion(filled_prompt, max_tokens=300, temperature=0.2)
        if out:
            parsed = _parse_llm_interpretation(out, valid_ids)
            if parsed:
                return {**default_q, **parsed}
    out = _heuristic_interpret(student_input, valid_ids)
    return {**default_q, **out}


def _parse_llm_interpretation(raw: str, valid_ids: set[str]) -> dict | None:
    """Try to extract topic, units, and multidimensional quality from LLM output."""
    raw = (raw or "").strip()
    # Try JSON block (allow nested for full object)
    json_match = re.search(r"\{[\s\S]*\"knowledge_units_taught\"[\s\S]*\}", raw)
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
            if not (isinstance(quality, (int, float)) and 0 <= quality <= 1):
                quality = 0.7
            acc = data.get("quality_accuracy", quality)
            comp = data.get("quality_completeness", quality)
            clarity = data.get("quality_clarity", quality)
            mis_corr = data.get("misconception_correction", False)
            interp = data.get("interpretation_class", INTERPRETATION_CORRECT if units else INTERPRETATION_AMBIGUOUS)
            if interp not in (INTERPRETATION_CORRECT, INTERPRETATION_INCORRECT, INTERPRETATION_AMBIGUOUS):
                interp = INTERPRETATION_AMBIGUOUS
            return {
                "topic_taught": topic or "Teaching",
                "knowledge_units_taught": units[:20],
                "quality_score": float(quality),
                "quality_accuracy": float(acc) if isinstance(acc, (int, float)) else 0.6,
                "quality_completeness": float(comp) if isinstance(comp, (int, float)) else 0.5,
                "quality_clarity": float(clarity) if isinstance(clarity, (int, float)) else 0.6,
                "misconception_correction": bool(mis_corr),
                "interpretation_class": interp,
            }
        except json.JSONDecodeError:
            pass
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
            "quality_accuracy": 0.7,
            "quality_completeness": 0.6,
            "quality_clarity": 0.7,
            "misconception_correction": False,
            "interpretation_class": INTERPRETATION_CORRECT if units else INTERPRETATION_AMBIGUOUS,
        }
    return None


def _heuristic_interpret(student_input: str, valid_ids: set[str]) -> dict:
    """Simple keyword heuristic when LLM is not used or fails. Includes default quality dimensions."""
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
    if "wrong" in text or "mistake" in text or "correct" in text or "remediation" in text:
        mis_corr = True
    else:
        mis_corr = False
    if not units and valid_ids:
        units = [next(iter(valid_ids))]
    score = 0.6 if units else 0.3
    return {
        "topic_taught": (student_input or "Teaching")[:200],
        "knowledge_units_taught": units[:20],
        "quality_score": score,
        "quality_accuracy": score,
        "quality_completeness": 0.5 if units else 0.3,
        "quality_clarity": 0.6,
        "misconception_correction": mis_corr,
        "interpretation_class": INTERPRETATION_CORRECT if units else INTERPRETATION_AMBIGUOUS,
    }
