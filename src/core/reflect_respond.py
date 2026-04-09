"""
Reflect-Respond pipeline for knowledge-state-constrained TA responses.
Four steps: Extract new knowledge from conversation -> Update reflection store
-> Retrieve relevant knowledge -> Generate response using only retrieved content.
"""

from __future__ import annotations

import json
import re
from typing import Any

from src.llm.client import llm_completion, llm_completion_stream


def _last_n_messages(conversation_history: list[dict], student_input: str, n: int = 5) -> list[dict]:
    """Last n turns plus the current student input."""
    out = list(conversation_history[-n:]) if conversation_history else []
    out.append({"role": "student", "content": student_input})
    return out


def extract_new_knowledge(
    messages: list[dict],
    domain: str,
    *,
    max_facts: int = 5,
    max_code: int = 2,
) -> dict[str, list]:
    """
    Step 1 (Reflect): Use LLM to extract new facts and code snippets from the latest conversation.
    Returns {"facts": [...], "code_snippets": [...]}.
    """
    if not messages:
        return {"facts": [], "code_snippets": []}
    conv_text = "\n".join(
        f"{m.get('role', 'user')}: {(m.get('content') or '')[:300]}"
        for m in messages
    )
    prompt = f"""You are analyzing a teaching conversation in a {domain} programming/concept domain.
From the conversation below, extract:
1) New factual knowledge the student taught (short statements the learner now "believes").
2) Any code snippets or implementation ideas the student demonstrated.

Output JSON only, with two keys: "facts" (list of strings, max {max_facts}), "code_snippets" (list of strings, max {max_code}).
If nothing new was taught, return {{"facts": [], "code_snippets": []}}.

Conversation:
{conv_text}

JSON:"""
    out = llm_completion(prompt, max_tokens=400, temperature=0.2)
    if not out:
        return {"facts": [], "code_snippets": []}
    raw = (out or "").strip()
    json_match = re.search(r"\{[\s\S]*\}", raw)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            facts = data.get("facts", [])
            code_snippets = data.get("code_snippets", [])
            if isinstance(facts, list):
                facts = [str(f).strip() for f in facts if f][:max_facts]
            else:
                facts = []
            if isinstance(code_snippets, list):
                code_snippets = [str(c).strip() for c in code_snippets if c][:max_code]
            else:
                code_snippets = []
            return {"facts": facts, "code_snippets": code_snippets}
        except json.JSONDecodeError:
            pass
    return {"facts": [], "code_snippets": []}


def update_reflection_store(
    store: dict,
    extracted: dict,
    *,
    max_facts_total: int = 30,
    max_code_total: int = 15,
) -> dict:
    """
    Step 2 (Update): Merge extracted knowledge into the reflection store.
    Does not call LLM. Returns updated store (new dict).
    """
    facts = list(store.get("facts", []))
    code_implementations = list(store.get("code_implementations", []))
    for f in extracted.get("facts", []):
        if f and f not in facts:
            facts.append(f)
    for c in extracted.get("code_snippets", []):
        if c and c not in code_implementations:
            code_implementations.append(c)
    return {
        "facts": facts[-max_facts_total:],
        "code_implementations": code_implementations[-max_code_total:],
    }


def retrieve_relevant(
    store: dict,
    teaching_topic: str,
    teaching_note: str,
    domain: str,
    *,
    learned_unit_ids: list[str] | None = None,
    active_misconceptions: list[str] | None = None,
) -> dict[str, list]:
    """
    Step 3 (Retrieve): Get knowledge from store relevant to the current teaching context.
    Uses LLM to select relevant facts and code, or falls back to keyword match.
    """
    facts = store.get("facts", [])
    code_impl = store.get("code_implementations", [])
    if not facts and not code_impl:
        return {"facts": [], "code_implementations": []}
    learned_unit_ids = learned_unit_ids or []
    active_misconceptions = active_misconceptions or []
    context = f"Topic: {teaching_topic}. Student said: {(teaching_note or '')[:200]}"
    prompt = f"""Given this teaching context in {domain}:
{context}

Learner constraints:
- Learned unit IDs (do not go beyond these): {", ".join(sorted(learned_unit_ids)[:20]) or "None"}
- Active misconceptions to focus/clarify: {", ".join(active_misconceptions[:20]) or "None"}

From the following stored knowledge, list only the items that are relevant to responding as a learner (restating or asking about this topic).
Reply with JSON: {{"relevant_facts": [indices or sublist], "relevant_code": [indices or sublist]}}
Or reply: {{"relevant_facts": [], "relevant_code": []}} if none apply.

Stored facts:
{chr(10).join(f'{i}: {f[:100]}' for i, f in enumerate(facts[:15]))}

Stored code snippets:
{chr(10).join(f'{i}: {c[:80]}...' for i, c in enumerate(code_impl[:10]))}

JSON:"""
    out = llm_completion(prompt, max_tokens=150, temperature=0.1)
    relevant_facts = []
    relevant_code = []
    if out:
        json_match = re.search(r"\{[\s\S]*\}", out.strip())
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                rf = data.get("relevant_facts", [])
                rc = data.get("relevant_code", [])
                if isinstance(rf, list):
                    for i in rf:
                        if isinstance(i, int) and 0 <= i < len(facts):
                            relevant_facts.append(facts[i])
                        elif isinstance(i, str) and i in facts:
                            relevant_facts.append(i)
                if isinstance(rc, list):
                    for i in rc:
                        if isinstance(i, int) and 0 <= i < len(code_impl):
                            relevant_code.append(code_impl[i])
                        elif isinstance(i, str) and i in code_impl:
                            relevant_code.append(i)
            except json.JSONDecodeError:
                pass
    if not relevant_facts and facts and (teaching_topic or teaching_note):
        topic_lower = (teaching_topic + " " + teaching_note).lower()
        for f in facts[-5:]:
            if any(w in f.lower() for w in topic_lower.split()[:5]):
                relevant_facts.append(f)
                break
    if active_misconceptions and facts:
        mis_matches = [f for f in facts if any(mid.lower() in f.lower() for mid in active_misconceptions)]
        for f in mis_matches:
            if f not in relevant_facts:
                relevant_facts.append(f)
    if not relevant_code and code_impl and (teaching_topic or teaching_note):
        relevant_code = code_impl[-2:]
    if learned_unit_ids:
        allowed_tokens = {u.lower() for u in learned_unit_ids}
        filtered = []
        for fact in relevant_facts:
            lowered = fact.lower()
            if any(tok in lowered for tok in allowed_tokens) or len(allowed_tokens) == 0:
                filtered.append(fact)
        if filtered:
            relevant_facts = filtered
    return {"facts": relevant_facts[:10], "code_implementations": relevant_code[:5]}


def generate_constrained_response(
    retrieved: dict,
    teaching_topic: str,
    teaching_note: str,
    learned_unit_ids: list[str],
    active_misconceptions: list[str],
    domain: str,
    conversation_history: list[dict] | None = None,
    *,
    ask_why_or_how: bool = True,
    prompt_rules: str | None = None,
) -> str:
    """
    Step 4 (Respond): Generate TA response using ONLY retrieved knowledge.
    If nothing retrieved, respond with "I'm not sure how to do that. Could you explain it to me?"
    """
    facts = retrieved.get("facts", [])
    code_impl = retrieved.get("code_implementations", [])
    learned_str = ", ".join(sorted(learned_unit_ids)[:20])
    mis_str = ", ".join(active_misconceptions) if active_misconceptions else "None"
    knowledge_block = "No knowledge yet."
    if facts or code_impl:
        knowledge_block = "Relevant facts you may use:\n" + "\n".join(f"- {f}" for f in facts[:8])
        if code_impl:
            knowledge_block += "\nRelevant code you know:\n" + "\n".join(f"- {c[:200]}" for c in code_impl[:3])
    else:
        knowledge_block = (
            "You have no relevant knowledge retrieved. "
            "Respond with exactly: I'm not sure how to do that. Could you explain it to me?"
        )

    history_block = ""
    if conversation_history:
        turns = conversation_history[-4:]
        history_block = "Recent conversation:\n" + "\n".join(
            f"{t.get('role', '')}: {(t.get('content') or '')[:150]}"
            for t in turns
        )

    extra_rules = ""
    if prompt_rules:
        extra_rules = f"\nAdditional behavior rules (must follow):\n{prompt_rules[:1800]}\n"

    prompt = f"""You are a novice learner in {domain}. The student just taught you something.
Strict: You may ONLY use the following knowledge in your response. Do not add external knowledge.

{knowledge_block}

Learned unit IDs (for reference): {learned_str}
Active misconceptions (you may express confusion): {mis_str}
Topic the student just taught: {teaching_topic}
What they said: {(teaching_note or '')[:300]}

{history_block}
{extra_rules}

Write 1-2 short sentences as the learner. Restate what you think you learned or ask a short "why" or "how" question.
Output only the TA reply, nothing else."""

    if ask_why_or_how and not knowledge_block.startswith("You have no"):
        prompt += "\nEnd with a short 'why' or 'how' question if natural."

    out = llm_completion(prompt, max_tokens=120, temperature=0.4)
    if out:
        out = (out or "").strip()
        if len(out) > 400:
            out = out[:397].rsplit(".", 1)[0] + "."
        return out
    if not facts and not code_impl:
        return "I'm not sure how to do that. Could you explain it to me?"
    return "I think I'm starting to get it. Can you give me an example?"


def _emotional_tone_context(
    teaching_note: str,
    quality_score: float | None,
    has_misconceptions: bool,
    learned_count: int,
) -> str:
    """Generate emotional tone guidance based on teaching context."""
    tone_rules = []
    # M-82: Emotional response based on context
    if quality_score is not None:
        if quality_score >= 0.8:
            tone_rules.append("Show genuine enthusiasm and gratitude: 'Ah, I see! Thank you for explaining so clearly.'")
        elif quality_score >= 0.5:
            tone_rules.append("Show cautious optimism: 'I think I'm getting it... let me see if I understand.'")
        else:
            tone_rules.append("Express genuine confusion and ask for help: 'I'm a bit confused about this. Could you explain it differently?'")
    if has_misconceptions:
        tone_rules.append("When confused by a misconception, express uncertainty honestly: 'I tried what you said but it doesn't seem right...'")
    if learned_count == 0:
        tone_rules.append("Show curiosity as a complete beginner: 'I'm new to this, so please bear with me!'")
    return "\n".join(tone_rules) if tone_rules else "Be friendly and show genuine curiosity about learning."


def _dynamic_max_tokens(teaching_note: str, has_code: bool, quality_score: float | None) -> int:
    """M-84: Dynamic reply length based on context."""
    note_len = len(teaching_note or "")
    # Simple confirmation should be short
    if note_len < 20 and not has_code:
        return 60
    # Detailed explanation with code can be longer
    if has_code and note_len > 100:
        return 200
    # Good quality teaching can have medium response
    if quality_score and quality_score >= 0.7:
        return 100
    return 120


def generate_constrained_response_stream(
    retrieved: dict,
    teaching_topic: str,
    teaching_note: str,
    learned_unit_ids: list[str],
    active_misconceptions: list[str],
    domain: str,
    conversation_history: list[dict] | None = None,
    *,
    ask_why_or_how: bool = True,
    prompt_rules: str | None = None,
    quality_score: float | None = None,
):
    """Step 4 (Respond) as a generator yielding text chunks with thinking steps (M-81)."""
    facts = retrieved.get("facts", [])
    code_impl = retrieved.get("code_implementations", [])
    learned_str = ", ".join(sorted(learned_unit_ids)[:20])
    mis_str = ", ".join(active_misconceptions) if active_misconceptions else "None"
    knowledge_block = "No knowledge yet."
    if facts or code_impl:
        knowledge_block = "Relevant facts you may use:\n" + "\n".join(f"- {f}" for f in facts[:8])
        if code_impl:
            knowledge_block += "\nRelevant code you know:\n" + "\n".join(f"- {c[:200]}" for c in code_impl[:3])
    else:
        knowledge_block = (
            "You have no relevant knowledge retrieved. "
            "Respond with exactly: I'm not sure how to do that. Could you explain it to me?"
        )
    history_block = ""
    if conversation_history:
        turns = conversation_history[-4:]
        history_block = "Recent conversation:\n" + "\n".join(
            f"{t.get('role', '')}: {(t.get('content') or '')[:150]}"
            for t in turns
        )
    extra_rules = ""
    if prompt_rules:
        extra_rules = f"\nAdditional behavior rules (must follow):\n{prompt_rules[:1800]}\n"

    # M-82: Emotional tone context
    has_misconceptions = bool(active_misconceptions)
    emotional_context = _emotional_tone_context(teaching_note, quality_score, has_misconceptions, len(learned_unit_ids))

    # M-84: Dynamic length control
    has_code = bool(code_impl) or "```" in (teaching_note or "") or "code" in (teaching_topic or "").lower()
    max_tokens = _dynamic_max_tokens(teaching_note, has_code, quality_score)

    # M-81: Add thinking process as a separate initial chunk
    thinking_messages = [
        "🤔 Let me think about what you just taught me...",
        "💭 I'm trying to understand this concept...",
        "📚 Let me recall what I've learned before...",
    ]
    # Select thinking message based on context
    if not facts and not code_impl:
        thinking_msg = "🤔 I'm not sure I have enough knowledge about this yet..."
    elif has_misconceptions:
        thinking_msg = "🤔 Hmm, this seems a bit confusing based on what I understood before..."
    elif quality_score and quality_score >= 0.8:
        thinking_msg = "💡 Oh! This is starting to make sense to me!"
    else:
        thinking_msg = thinking_messages[len(teaching_note or "") % len(thinking_messages)]

    yield f"[THINKING]{thinking_msg}[/THINKING]"

    prompt = f"""You are a novice learner in {domain}. The student just taught you something.
Strict: You may ONLY use the following knowledge in your response. Do not add external knowledge.

{knowledge_block}

Learned unit IDs (for reference): {learned_str}
Active misconceptions (you may express confusion): {mis_str}
Topic the student just taught: {teaching_topic}
What they said: {(teaching_note or '')[:300]}

{history_block}
{extra_rules}

Emotional tone guidance:
{emotional_context}

Write 1-2 short sentences as the learner. Restate what you think you learned or ask a short "why" or "how" question.
Output only the TA reply, nothing else."""
    if ask_why_or_how and not knowledge_block.startswith("You have no"):
        prompt += "\nEnd with a short 'why' or 'how' question if natural."

    full: list[str] = []
    for delta in llm_completion_stream(prompt, max_tokens=max_tokens, temperature=0.4):
        full.append(delta)
        yield delta
    out = "".join(full).strip() if full else ""
    if not out and not facts and not code_impl:
        out = "I'm not sure how to do that. Could you explain it to me?"
    elif not out:
        out = "I think I'm starting to get it. Can you give me an example?"
    # Dynamic length limit based on complexity
    if len(out) > max_tokens:
        out = out[:max_tokens-3].rsplit(".", 1)[0] + "."


def run_reflect_respond_pipeline(
    reflection_store: dict,
    teaching_event: dict,
    learned_unit_ids: list[str],
    active_misconceptions: list[str],
    domain: str,
    conversation_history: list[dict] | None = None,
    student_input: str | None = None,
    *,
    use_llm: bool = True,
) -> tuple[str, dict]:
    """
    Run the full Reflect-Respond pipeline.
    Returns (ta_response: str, updated_reflection_store: dict).
    If use_llm is False or LLM unavailable, returns fallback response and unchanged store.
    """
    topic = teaching_event.get("topic_taught", "")
    note = teaching_event.get("note", "") or student_input or ""
    store = dict(reflection_store) if reflection_store else {"facts": [], "code_implementations": []}
    messages = _last_n_messages(conversation_history or [], note, n=5)

    if not use_llm:
        return (
            "I think I'm starting to get it. Can you give me an example?",
            store,
        )

    # Step 1: Extract
    extracted = extract_new_knowledge(messages, domain)
    # Step 2: Update store with extracted knowledge
    store = update_reflection_store(store, extracted)
    # Step 3: Retrieve from the updated store (avoids stale retrieval)
    retrieved = retrieve_relevant(
        store,
        topic,
        note,
        domain,
        learned_unit_ids=learned_unit_ids,
        active_misconceptions=active_misconceptions,
    )

    # Step 4: Respond – generate constrained response
    response = generate_constrained_response(
        retrieved,
        teaching_topic=topic,
        teaching_note=note,
        learned_unit_ids=learned_unit_ids,
        active_misconceptions=active_misconceptions,
        domain=domain,
        conversation_history=conversation_history,
        ask_why_or_how=True,
    )
    return response, store
