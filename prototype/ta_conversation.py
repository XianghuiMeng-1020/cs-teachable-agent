"""
Stage One: Controlled conversation layer — TA learner-style response during teaching.
Constrained by current knowledge state; no tutoring; no concepts outside learned units.
Uses LLM when available (OpenAI), else fallback stub so the demo always runs.
"""

import os
from pathlib import Path

# Prompt template path (relative to this file)
_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "ta_learner_conversation_prompt.md"

# Stage One scope: only these concept names may be referenced when learned
_STAGE_ONE_SCOPE_IDS = frozenset({
    "variable_assignment", "print_function", "user_input",
    "data_types_int_float", "data_types_string", "data_types_bool",
    "arithmetic_operators", "comparison_operators", "logical_operators", "string_concatenation",
    "if_statement", "if_else", "if_elif_else",
    "while_loop", "for_loop_range", "for_loop_iterable",
    "list_creation", "list_indexing", "list_basics", "list_iteration",
})


def _load_prompt_template() -> str:
    """Load the learner conversation prompt template."""
    if _PROMPT_PATH.exists():
        return _PROMPT_PATH.read_text(encoding="utf-8")
    return ""


def _fill_prompt(
    learned_unit_ids: set[str],
    teaching_event: dict,
    active_misconceptions: list[str] | None,
) -> str:
    """Fill the prompt template with current state. Only include learned units that are in Stage One scope."""
    allowed_learned = sorted(learned_unit_ids & _STAGE_ONE_SCOPE_IDS)
    topic = teaching_event.get("topic_taught", "")
    note = teaching_event.get("note", "")
    mis = active_misconceptions or []
    mis_str = ", ".join(mis) if mis else "None"

    template = _load_prompt_template()
    return (
        template.replace("{{LEARNED_UNITS}}", ", ".join(allowed_learned))
        .replace("{{TEACHING_TOPIC}}", topic)
        .replace("{{TEACHING_NOTE}}", note)
        .replace("{{ACTIVE_MISCONCEPTIONS}}", mis_str)
    )


def _fallback_stub_response(
    teaching_event: dict,
    learned_unit_ids: set[str],
    active_misconceptions: list[str] | None = None,
) -> str:
    """
    Return a short learner-style response without calling an LLM.
    Only mentions concepts in learned_unit_ids; stays within Stage One scope.
    When active_misconceptions is non-empty, may reflect slight confusion (Stage C).
    """
    topic = (teaching_event.get("topic_taught") or "").lower()
    units = learned_unit_ids & _STAGE_ONE_SCOPE_IDS
    mis = active_misconceptions or []

    if mis and ("variable" in topic or "print" in topic or "variable_assignment" in units or "print_function" in units):
        return "I think I get it, but I might still mix up what to print sometimes."

    if "print" in topic or "print_function" in units:
        if "variable" in topic or "variable_assignment" in units:
            return "So I can put a value in a variable and then print it with print()?"
        return "I think print() is how I show something on the screen."
    if "variable" in topic or "variable_assignment" in units:
        return "So x = 5 means the variable stores the value 5?"
    if "input" in topic or "user_input" in units:
        return "So input() reads what the user types, and I can put it in a variable?"
    if "loop" in topic or "for_loop_range" in units or "while_loop" in units:
        return "I'm still a bit confused about when to use for versus while."
    if "if" in topic or "condition" in topic or "if_statement" in units:
        return "So if the condition is true, the code inside runs?"
    if "list" in topic or "list_creation" in units:
        return "So a list holds several values in order, like [1, 2, 3]?"

    # Generic fallback: restate the topic briefly
    if units:
        return f"I think I'm starting to get it. You taught me about {topic or 'this'}."
    return "I don't know that yet. Can you explain it again?"


def _call_openai(prompt: str, max_tokens: int = 80) -> str | None:
    """Call OpenAI Chat Completions if API key is set. Returns None on failure or missing key."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.4,
        )
        text = (response.choices[0].message.content or "").strip()
        # Keep to 1–2 sentences; truncate if model returned too much
        if len(text) > 300:
            text = text[:297].rsplit(".", 1)[0] + "."
        return text or None
    except Exception:
        return None


def get_ta_learner_response(
    learned_unit_ids: set[str],
    teaching_event: dict,
    active_misconceptions: list[str] | None = None,
    *,
    use_llm: bool | None = None,
) -> str:
    """
    Generate a short TA learner-style response after a teaching event.

    - learned_unit_ids: only these concepts may be referenced (knowledge-state control).
    - teaching_event: dict with topic_taught, knowledge_units_taught, note.
    - active_misconceptions: optional list of misconception ids (may express confusion).
    - use_llm: if True, try LLM; if False, use stub only; if None, try LLM then fallback.

    Returns a short string (1–2 sentences). Never teaches or uses concepts outside
    learned_unit_ids; never mentions concepts outside Stage One scope.
    """
    # Enforce: only Stage One units are passed through to the prompt
    allowed = learned_unit_ids & _STAGE_ONE_SCOPE_IDS
    prompt = _fill_prompt(allowed, teaching_event, active_misconceptions)
    mis_list = list(active_misconceptions) if active_misconceptions else None

    if use_llm is False:
        return _fallback_stub_response(teaching_event, allowed, mis_list)

    if use_llm is True:
        out = _call_openai(prompt)
        if out:
            return out
        return _fallback_stub_response(teaching_event, allowed, mis_list)

    # use_llm is None: try LLM first, then fallback
    out = _call_openai(prompt)
    if out:
        return out
    return _fallback_stub_response(teaching_event, allowed, mis_list)
