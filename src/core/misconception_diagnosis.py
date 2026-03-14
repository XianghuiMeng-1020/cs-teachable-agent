"""
LLM-assisted misconception diagnosis: from teaching input and from failed attempts.
Falls back to pattern-based inference when LLM is unavailable.
"""

from pathlib import Path
import json

from src.llm.client import llm_completion

_DIAG_PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def _load_prompt(name: str) -> str:
    path = _DIAG_PROMPTS_DIR / f"{name}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def diagnose_from_teaching(
    student_input: str,
    known_unit_ids: list[str],
    misconceptions_catalog: list[dict],
    *,
    filled_prompt: str | None = None,
    use_llm: bool = True,
) -> dict:
    """
    Analyze student teaching input for incorrect or ambiguous content that might
    induce a misconception. Returns interpretation with optional matched misconception.
    """
    if not student_input or not known_unit_ids:
        return {
            "interpretation": "unknown",
            "misconception_id": None,
            "affected_unit_ids": [],
            "confidence": 0.0,
            "reason": "No input or units.",
        }
    if use_llm and filled_prompt:
        template = filled_prompt
    elif use_llm:
        template = _load_prompt("diagnose_from_teaching")
        if template:
            mis_list = ", ".join(m.get("id", "") for m in misconceptions_catalog)
            units_list = ", ".join(known_unit_ids)
            template = (
                template.replace("{{STUDENT_INPUT}}", student_input[:1500])
                .replace("{{KNOWN_UNIT_IDS}}", units_list)
                .replace("{{MISCONCEPTION_IDS}}", mis_list)
            )
    else:
        return {"interpretation": "unknown", "misconception_id": None, "affected_unit_ids": [], "confidence": 0.0, "reason": "LLM not used."}

    if not template:
        return {"interpretation": "unknown", "misconception_id": None, "affected_unit_ids": [], "confidence": 0.0, "reason": "No prompt."}

    out = llm_completion(template, max_tokens=200, temperature=0.1)
    if not out:
        return {"interpretation": "unknown", "misconception_id": None, "affected_unit_ids": [], "confidence": 0.0, "reason": "LLM unavailable."}

    try:
        text = (out or "").strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        data = json.loads(text)
        interpretation = data.get("interpretation", "unknown")
        misconception_id = data.get("misconception_id")
        affected_unit_ids = data.get("affected_unit_ids") or []
        confidence = float(data.get("confidence", 0.0))
        reason = data.get("reason", "")
        if interpretation not in ("correct", "incorrect", "ambiguous", "unknown"):
            interpretation = "unknown"
        return {
            "interpretation": interpretation,
            "misconception_id": misconception_id,
            "affected_unit_ids": affected_unit_ids,
            "confidence": max(0.0, min(1.0, confidence)),
            "reason": reason,
        }
    except (json.JSONDecodeError, TypeError, ValueError):
        return {"interpretation": "unknown", "misconception_id": None, "affected_unit_ids": [], "confidence": 0.0, "reason": "Parse error."}


def diagnose_from_failed_attempt(
    ta_code_or_answer: str,
    problem: dict,
    misconceptions_catalog: list[dict],
    *,
    filled_prompt: str | None = None,
    use_llm: bool = True,
    fallback_to_pattern: bool = True,
):
    """
    Infer likely misconceptions from a failed TA attempt (code or answer).
    When use_llm and filled_prompt are set, calls LLM; else or on failure
    falls back to pattern-based infer_misconception_from_failed_attempt.
    Returns list of (misconception_id, unit_id, confidence).
    """
    from src.core.misconception_engine import infer_misconception_from_failed_attempt as pattern_infer

    result_tuples: list[tuple[str, str, float]] = []

    if use_llm and (filled_prompt or _load_prompt("diagnose_from_failed_attempt")):
        template = filled_prompt or _load_prompt("diagnose_from_failed_attempt")
        if template and ta_code_or_answer:
            statement = problem.get("problem_statement", "")
            units_tested = problem.get("knowledge_units_tested", [])
            mis_list = json.dumps([{"id": m.get("id"), "description": m.get("description", "")[:80]} for m in misconceptions_catalog])
            template = (
                template.replace("{{TA_CODE_OR_ANSWER}}", (ta_code_or_answer or "")[:1200])
                .replace("{{PROBLEM_STATEMENT}}", statement[:500])
                .replace("{{UNITS_TESTED}}", json.dumps(units_tested))
                .replace("{{MISCONCEPTIONS}}", mis_list)
            )
            out = llm_completion(template, max_tokens=250, temperature=0.1)
            if out:
                try:
                    text = (out or "").strip()
                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0].strip()
                    data = json.loads(text)
                    candidates = data.get("candidates") or data.get("inferred") or []
                    for c in candidates[:3]:
                        mid = c.get("misconception_id") or c.get("id")
                        uid = (c.get("affected_unit_id") or c.get("unit_id") or (units_tested or [None])[0])
                        conf = float(c.get("confidence", 0.5))
                        if mid and uid:
                            result_tuples.append((mid, uid, max(0.0, min(1.0, conf))))
                except (json.JSONDecodeError, TypeError, ValueError, KeyError):
                    pass

    if fallback_to_pattern and not result_tuples:
        result_tuples = pattern_infer(
            ta_code_or_answer,
            problem,
            misconceptions_catalog,
            min_confidence=0.5,
        )

    result_tuples.sort(key=lambda x: -x[2])
    return result_tuples[:5]
