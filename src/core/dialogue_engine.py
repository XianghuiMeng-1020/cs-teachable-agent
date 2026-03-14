"""
TA learner-style response during teaching. Multi-strategy: Reflect-Respond, Socratic,
Elaboration, Confusion. Strictly constrained by knowledge state; no tutoring.
"""

from src.llm.client import llm_completion

STRATEGY_REFLECT_RESPOND = "reflect_respond"
STRATEGY_SOCRATIC = "socratic"
STRATEGY_ELABORATION = "elaboration"
STRATEGY_CONFUSION = "confusion"
DEFAULT_STRATEGY = STRATEGY_REFLECT_RESPOND

# Stage One scope: only these concept names may be referenced when learned
_STAGE_ONE_SCOPE_IDS = frozenset({
    "variable_assignment", "print_function", "user_input",
    "data_types_int_float", "data_types_string", "data_types_bool",
    "arithmetic_operators", "comparison_operators", "logical_operators", "string_concatenation",
    "if_statement", "if_else", "if_elif_else",
    "while_loop", "for_loop_range", "for_loop_iterable",
    "list_creation", "list_indexing", "list_basics", "list_iteration",
})


def _reflect_respond(
    reflect: str,
    ask_why_or_how: bool = True,
) -> str:
    """Format as Reflect-Respond: '[Reflect]. [Why/How ...?]'"""
    if not ask_why_or_how or not reflect.strip():
        return reflect.strip()
    if reflect.rstrip().endswith("?"):
        return reflect.strip()
    return reflect.strip() + " Why is that? Or how do I use it?"


def _strategy_suffix(strategy: str) -> str:
    """Optional instruction suffix for LLM per strategy."""
    if strategy == STRATEGY_SOCRATIC:
        return "\nRespond as a curious learner: ask a short 'why' or 'how' question (e.g. 'Why do we use == instead of = here?')."
    if strategy == STRATEGY_ELABORATION:
        return "\nRespond as a learner: ask for one concrete example (e.g. 'Can you give me an example?')."
    if strategy == STRATEGY_CONFUSION:
        return "\nRespond as a confused learner: briefly say something seems inconsistent or unclear (e.g. 'Wait, that seems different from what you said before.')."
    return ""


def _select_strategy(learned_count: int, has_active_misconceptions: bool) -> str:
    """Choose strategy from knowledge state: more confusion when misconceptions active."""
    if has_active_misconceptions and learned_count > 2:
        return STRATEGY_CONFUSION
    if learned_count <= 1:
        return STRATEGY_ELABORATION
    return STRATEGY_REFLECT_RESPOND


def _fallback_stub_response(
    teaching_event: dict,
    learned_unit_ids: set[str],
    active_misconceptions: list[str] | None = None,
    *,
    use_reflect_respond: bool = True,
) -> str:
    """Return a short learner-style response; Reflect-Respond when requested."""
    topic = (teaching_event.get("topic_taught") or "").lower()
    units = learned_unit_ids & _STAGE_ONE_SCOPE_IDS
    mis = active_misconceptions or []
    reflect = ""

    if mis and (
        "variable" in topic
        or "print" in topic
        or "variable_assignment" in units
        or "print_function" in units
    ):
        reflect = "I think I get it, but I might still mix up what to print sometimes."

    elif "print" in topic or "print_function" in units:
        if "variable" in topic or "variable_assignment" in units:
            reflect = "So I can put a value in a variable and then print it with print()."
        else:
            reflect = "I think print() is how I show something on the screen."
    elif "variable" in topic or "variable_assignment" in units:
        reflect = "So x = 5 means the variable stores the value 5."
    elif "input" in topic or "user_input" in units:
        reflect = "So input() reads what the user types, and I can put it in a variable."
    elif "loop" in topic or "for_loop_range" in units or "while_loop" in units:
        reflect = "I'm still a bit confused about when to use for versus while."
    elif "if" in topic or "condition" in topic or "if_statement" in units:
        reflect = "So if the condition is true, the code inside runs?"
    elif "list" in topic or "list_creation" in units:
        reflect = "So a list holds several values in order, like [1, 2, 3]."
    elif units:
        reflect = f"I think I'm starting to get it. You taught me about {topic or 'this'}."
    else:
        reflect = "I don't know that yet. Can you explain it again?"

    if use_reflect_respond and reflect and "?" not in reflect:
        return _reflect_respond(reflect, ask_why_or_how=True)
    return reflect


def _build_prompt_with_history(filled_prompt: str, conversation_history: list[dict] | None, max_turns: int = 5) -> str:
    """Prepend recent conversation turns to the prompt for context."""
    if not conversation_history or not filled_prompt:
        return filled_prompt
    turns = conversation_history[-max_turns:]
    lines = ["Recent conversation (student then TA):"]
    for t in turns:
        role = (t.get("role") or "user").lower()
        content = (t.get("content") or "")[:200]
        lines.append(f"- {role}: {content}")
    lines.append("\nNow generate the TA's next response (one or two short sentences):\n")
    return "\n".join(lines) + filled_prompt


def get_ta_learner_response(
    learned_unit_ids: set[str],
    teaching_event: dict,
    active_misconceptions: list[str] | None = None,
    *,
    filled_prompt: str | None = None,
    use_llm: bool | None = None,
    use_reflect_respond: bool = True,
    conversation_history: list[dict] | None = None,
    strategy: str | None = None,
) -> str:
    """
    Generate TA learner-style response after a teaching event. Constrained by knowledge state:
    only reference concepts in learned_unit_ids; exhibit confusion or errors for active_misconceptions.
    Strategies: reflect_respond, socratic, elaboration, confusion.
    - conversation_history: optional list of {role, content} for multi-turn context in prompt.
    """
    allowed = learned_unit_ids & _STAGE_ONE_SCOPE_IDS
    mis_list = list(active_misconceptions) if active_misconceptions else None

    if use_llm is False:
        return _fallback_stub_response(
            teaching_event, allowed, mis_list, use_reflect_respond=use_reflect_respond
        )

    if (use_llm is True or use_llm is None) and filled_prompt:
        prompt = _build_prompt_with_history(filled_prompt, conversation_history)
        if strategy is None:
            strategy = _select_strategy(len(learned_unit_ids), bool(mis_list))
        prompt = prompt.rstrip() + _strategy_suffix(strategy)
        out = llm_completion(prompt, max_tokens=120, temperature=0.4)
        if out:
            out = (out or "").strip()
            if len(out) > 400:
                out = out[:397].rsplit(".", 1)[0] + "."
            if use_reflect_respond and strategy == STRATEGY_REFLECT_RESPOND and out and "?" not in out:
                out = _reflect_respond(out, ask_why_or_how=True)
            return out
        return _fallback_stub_response(
            teaching_event, allowed, mis_list, use_reflect_respond=use_reflect_respond
        )
    return _fallback_stub_response(
        teaching_event, allowed, mis_list, use_reflect_respond=use_reflect_respond
    )


def get_reflection_prompt_after_test(
    problem_statement: str,
    passed: bool,
    ta_code_or_answer: str | None = None,
) -> str:
    """
    Return a short reflection question for the student after a test attempt.
    """
    if passed:
        return "What do you think helped the TA get this one right?"
    return "Why do you think the TA made a mistake here? What would you re-teach?"
