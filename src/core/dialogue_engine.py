"""
TA learner-style response during teaching. Constrained by knowledge state; no tutoring.
Uses LLM when filled_prompt is provided and use_llm; else stub.
"""

from src.llm.client import llm_completion

# Stage One scope: only these concept names may be referenced when learned
_STAGE_ONE_SCOPE_IDS = frozenset({
    "variable_assignment", "print_function", "user_input",
    "data_types_int_float", "data_types_string", "data_types_bool",
    "arithmetic_operators", "comparison_operators", "logical_operators", "string_concatenation",
    "if_statement", "if_else", "if_elif_else",
    "while_loop", "for_loop_range", "for_loop_iterable",
    "list_creation", "list_indexing", "list_basics", "list_iteration",
})


def _fallback_stub_response(
    teaching_event: dict,
    learned_unit_ids: set[str],
    active_misconceptions: list[str] | None = None,
) -> str:
    """Return a short learner-style response without LLM."""
    topic = (teaching_event.get("topic_taught") or "").lower()
    units = learned_unit_ids & _STAGE_ONE_SCOPE_IDS
    mis = active_misconceptions or []

    if mis and (
        "variable" in topic
        or "print" in topic
        or "variable_assignment" in units
        or "print_function" in units
    ):
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

    if units:
        return f"I think I'm starting to get it. You taught me about {topic or 'this'}."
    return "I don't know that yet. Can you explain it again?"


def get_ta_learner_response(
    learned_unit_ids: set[str],
    teaching_event: dict,
    active_misconceptions: list[str] | None = None,
    *,
    filled_prompt: str | None = None,
    use_llm: bool | None = None,
) -> str:
    """
    Generate TA learner-style response after a teaching event.
    - filled_prompt: if provided and use_llm is True, call LLM with it.
    - use_llm: if True try LLM (when filled_prompt given); if False stub only; if None try LLM then fallback.
    """
    allowed = learned_unit_ids & _STAGE_ONE_SCOPE_IDS
    mis_list = list(active_misconceptions) if active_misconceptions else None

    if use_llm is False:
        return _fallback_stub_response(teaching_event, allowed, mis_list)

    if use_llm is True and filled_prompt:
        out = llm_completion(filled_prompt, max_tokens=80, temperature=0.4)
        if out:
            if len(out) > 300:
                out = out[:297].rsplit(".", 1)[0] + "."
            return out
        return _fallback_stub_response(teaching_event, allowed, mis_list)

    if use_llm is None and filled_prompt:
        out = llm_completion(filled_prompt, max_tokens=80, temperature=0.4)
        if out:
            if len(out) > 300:
                out = out[:297].rsplit(".", 1)[0] + "."
            return out
    return _fallback_stub_response(teaching_event, allowed, mis_list)
