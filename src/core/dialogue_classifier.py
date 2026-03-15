"""
Dialogue quality classifier: label each message as knowledge-telling vs knowledge-building
(TeachYou taxonomy). Used for research analytics and TraceEvent storage.
"""

from __future__ import annotations

from src.llm.client import llm_completion

LABEL_KNOWLEDGE_TELLING = "knowledge_telling"
LABEL_KNOWLEDGE_BUILDING = "knowledge_building"
LABEL_OTHER = "other"


def classify_message(
    role: str,
    content: str,
    *,
    domain: str = "python",
) -> str:
    """
    Classify a single message: knowledge_telling (instruction/prompting/statement without elaboration)
    vs knowledge_building (explanation, examples, why/how, scaffolding).
    Returns one of: knowledge_telling, knowledge_building, other.
    """
    if not (content or "").strip():
        return LABEL_OTHER
    prompt = f"""Classify this teaching message in a {domain} learning-by-teaching setting.

Message (role: {role}):
{content[:500]}

Labels:
- knowledge_telling: The student gives instructions, prompts, or statements without explaining why or how (e.g. "write a loop", "use print()").
- knowledge_building: The student explains concepts, gives examples, asks the TA to reason, or scaffolds understanding (e.g. "we use a loop when we want to repeat; for example...").
- other: Unclear or off-topic.

Reply with exactly one word: knowledge_telling, knowledge_building, or other."""
    out = llm_completion(prompt, max_tokens=20, temperature=0.1)
    if not out:
        return LABEL_OTHER
    label = (out or "").strip().lower()
    if "knowledge_telling" in label:
        return LABEL_KNOWLEDGE_TELLING
    if "knowledge_building" in label:
        return LABEL_KNOWLEDGE_BUILDING
    return LABEL_OTHER
