"""
Mode-Shifting: TA periodically switches to Questioner mode to ask "why"/"how" questions,
scaffolding knowledge-building (TeachYou/AlgoBo style). Every N turns the TA asks
a thought-provoking question instead of only reflecting.
"""

from __future__ import annotations

from src.llm.client import llm_completion

# Every QUESTIONER_INTERVAL-th message (1-based), TA is in questioner mode
QUESTIONER_INTERVAL = 3


def should_ask_question(conversation_message_count: int) -> bool:
    """
    True if this turn should be in Questioner mode (every QUESTIONER_INTERVAL turns).
    conversation_message_count = number of messages so far (student + TA) before this response.
    So the next message is the (conversation_message_count + 1)-th; we want 3rd, 6th, 9th...
    """
    if conversation_message_count < 0:
        return False
    return (conversation_message_count + 1) % QUESTIONER_INTERVAL == 0


def generate_thought_provoking_question(
    teaching_topic: str,
    teaching_note: str,
    domain: str,
    learned_unit_ids: list[str],
    conversation_recent: list[dict],
    *,
    phase: str = "teach",
) -> str:
    """
    Generate a short "why" or "how" question to prompt the student to elaborate.
    phase: "teach" (concept/code) -> why/how questions; "discuss" -> how/real-world.
    """
    context = (teaching_topic or "") + " " + (teaching_note or "")[:200]
    recent = "\n".join(
        f"{m.get('role', '')}: {(m.get('content') or '')[:120]}"
        for m in conversation_recent[-4:]
    )
    prompt = f"""You are a novice learner in {domain}. You are asking your tutor a thought-provoking question
to understand better. The tutor just explained: {context}

Recent conversation:
{recent}

Learned concepts (for reference): {', '.join(sorted(learned_unit_ids)[:15])}

Generate exactly one short "why" or "how" question (e.g. "Why do we use == instead of = here?"
or "How would I use this in a real program?"). Output only the question, one sentence."""
    if phase == "discuss":
        prompt += "\nPrefer a 'how' question about applying the concept or a real-world example."
    out = llm_completion(prompt, max_tokens=60, temperature=0.5)
    if out:
        out = (out or "").strip()
        if out and out[-1] != "?":
            out = out + "?"
        return out[:150] if out else ""
    return "Why is that? Can you give me an example?"


def maybe_append_questioner_response(
    base_response: str,
    conversation_message_count: int,
    teaching_topic: str,
    teaching_note: str,
    domain: str,
    learned_unit_ids: list[str],
    conversation_history: list[dict] | None,
    *,
    phase: str = "teach",
) -> str:
    """
    If this turn is a Questioner turn, append a thought-provoking question to base_response.
    Returns the final TA response string.
    """
    if not should_ask_question(conversation_message_count):
        return base_response
    count = len(conversation_history) if conversation_history else 0
    question = generate_thought_provoking_question(
        teaching_topic,
        teaching_note,
        domain,
        list(learned_unit_ids),
        conversation_history or [],
        phase=phase,
    )
    if not question:
        return base_response
    if base_response.strip().endswith("?"):
        return base_response + " " + question
    return base_response.rstrip() + ". " + question
