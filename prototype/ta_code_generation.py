"""
Stage One: Controlled TA code generation — optional LLM path alongside stub.
- Only uses concepts from current learned knowledge state.
- Optional active misconceptions can lead to beginner-style errors.
- Output guard rejects out-of-scope code; fallback to stub on reject or LLM failure.
The existing stub path in ta_attempt.py is never removed; this module calls it as fallback.
"""

import os
import re
from pathlib import Path

_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "ta_code_generation_prompt.md"

# Forbidden patterns for Stage One (reject generated code containing these).
_FORBIDDEN_PATTERNS = [
    re.compile(r"\bdef\s+\w+", re.IGNORECASE),
    re.compile(r"\bclass\s+\w+", re.IGNORECASE),
    re.compile(r"\bimport\s+", re.IGNORECASE),
    re.compile(r"\bopen\s*\(", re.IGNORECASE),
    re.compile(r"\btry\s*:", re.IGNORECASE),
    re.compile(r"\bexcept\b", re.IGNORECASE),
    re.compile(r"\bwith\s+\w+\s+as\b", re.IGNORECASE),
]


def _load_prompt_template() -> str:
    if _PROMPT_PATH.exists():
        return _PROMPT_PATH.read_text(encoding="utf-8")
    return ""


def _fill_prompt(
    problem: dict,
    learned_unit_ids: set[str],
    active_misconceptions: list[str] | None,
) -> str:
    pid = problem.get("problem_id", "")
    statement = problem.get("problem_statement", "")
    input_spec = problem.get("input_spec") or "No input."
    units_str = ", ".join(sorted(learned_unit_ids))
    mis = active_misconceptions or []
    mis_str = ", ".join(mis) if mis else "None"

    template = _load_prompt_template()
    return (
        template.replace("{{PROBLEM_ID}}", pid)
        .replace("{{PROBLEM_STATEMENT}}", statement)
        .replace("{{INPUT_SPEC}}", str(input_spec))
        .replace("{{LEARNED_UNITS}}", units_str)
        .replace("{{ACTIVE_MISCONCEPTIONS}}", mis_str)
    )


def output_guard(code: str) -> bool:
    """
    Return True if the code is allowed (no Stage One forbidden constructs).
    Reject def, class, import, open(, try:, except, with...as.
    """
    if not code or not code.strip():
        return False
    for pat in _FORBIDDEN_PATTERNS:
        if pat.search(code):
            return False
    return True


def _extract_code(raw: str) -> str:
    """Strip markdown code fence if present; return trimmed code."""
    text = (raw or "").strip()
    if text.startswith("```"):
        # Remove first line (```python or ```) and trailing ```
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


def _generate_via_llm(
    problem: dict,
    learned_unit_ids: set[str],
    active_misconceptions: list[str] | None = None,
    max_tokens: int = 256,
) -> str | None:
    """Call OpenAI to generate code. Returns None on failure or missing key."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    prompt = _fill_prompt(problem, learned_unit_ids, active_misconceptions)
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.3,
        )
        raw = (response.choices[0].message.content or "").strip()
        code = _extract_code(raw)
        return code if code else None
    except Exception:
        return None


def get_ta_code_attempt(
    problem: dict,
    learned_unit_ids: set[str],
    active_misconceptions: list[str] | None = None,
    force_fail_problem_ids: set[str] | None = None,
    *,
    use_llm_code: bool | None = None,
) -> str:
    """
    Return TA code attempt for the problem. Parallel paths:
    - Stub path (ta_attempt.get_ta_attempt): always available, used when use_llm_code is False,
      when required KUs are missing, when force_fail is set for this problem, or when LLM/guard fails.
    - LLM path: when use_llm_code is True and API available; output is checked by output_guard;
      if guard fails or LLM fails, fallback to stub.

    - If required knowledge units are not all learned, returns stub no-attempt placeholder.
    - If force_fail_problem_ids contains this problem_id, uses stub wrong code (deterministic failure).
    - If use_llm_code and LLM returns valid (guard-passing) code, returns it; else stub.
    """
    from ta_attempt import get_ta_attempt

    required = set(problem.get("knowledge_units_tested", []))
    force_fail = force_fail_problem_ids or set()
    pid = problem.get("problem_id", "")

    active_mis_list = list(active_misconceptions) if active_misconceptions else None
    if not required <= learned_unit_ids:
        return get_ta_attempt(problem, learned_unit_ids, force_fail_problem_ids, active_mis_list)

    if pid in force_fail:
        return get_ta_attempt(problem, learned_unit_ids, force_fail_problem_ids, active_mis_list)

    if use_llm_code is not True:
        return get_ta_attempt(problem, learned_unit_ids, force_fail_problem_ids, active_mis_list)

    code = _generate_via_llm(problem, learned_unit_ids, active_misconceptions)
    if code and output_guard(code):
        return code
    return get_ta_attempt(problem, learned_unit_ids, force_fail_problem_ids, active_mis_list)
