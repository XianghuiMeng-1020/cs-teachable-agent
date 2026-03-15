"""
Teaching Helper: real-time metacognitive feedback on teaching quality.
Detects antipatterns: Commanding, Spoon-feeding, Under-teaching.
Returns feedback and suggestions for the student to improve.
"""

from __future__ import annotations

from src.llm.client import llm_completion

PATTERN_GOOD = "good"
PATTERN_COMMANDING = "commanding"
PATTERN_SPOON_FEEDING = "spoon_feeding"
PATTERN_UNDER_TEACHING = "under_teaching"


def analyze_teaching(
    recent_messages: list[dict],
    student_input: str,
    *,
    domain: str = "python",
) -> dict:
    """
    Analyze the last few turns + current student input for teaching antipatterns.
    Returns:
      pattern: one of "commanding" | "spoon_feeding" | "under_teaching" | "good"
      feedback: short explanation
      suggestions: list of strings (actions the student could take)
    """
    if not recent_messages and not student_input.strip():
        return {
            "pattern": PATTERN_GOOD,
            "feedback": "",
            "suggestions": [],
        }
    conv = "\n".join(
        f"{m.get('role', 'user')}: {(m.get('content') or '')[:200]}"
        for m in recent_messages[-6:]
    )
    prompt = f"""You are analyzing a student's teaching in a {domain} learning-by-teaching setting.
The student is teaching a virtual TA. Detect if the student's latest message shows one of these antipatterns:

1) **commanding**: The student only gives instructions or commands (e.g. "write a loop", "fix line 3") without explaining WHY or HOW. No conceptual explanation.

2) **spoon_feeding**: The student gives the answer or solution directly without checking if the TA understands, or without asking the TA to try first.

3) **under_teaching**: The student says very little or something vague; the TA would have to figure things out alone. No real teaching content.

If none of these fit, the teaching is **good** (student explains concepts, gives examples, or asks the TA to reason).

Conversation so far:
{conv}

Student's latest message:
{student_input[:400]}

Reply with JSON only:
{{"pattern": "commanding"|"spoon_feeding"|"under_teaching"|"good", "feedback": "one sentence explanation", "suggestions": ["suggestion 1", "suggestion 2"]}}
For "good", feedback can be empty and suggestions can be []. For antipatterns, give 1-2 concrete suggestions."""

    out = llm_completion(prompt, max_tokens=200, temperature=0.2)
    if not out:
        return {
            "pattern": PATTERN_GOOD,
            "feedback": "",
            "suggestions": [],
        }
    import json
    import re
    raw = (out or "").strip()
    m = re.search(r"\{[\s\S]*\}", raw)
    if m:
        try:
            data = json.loads(m.group(0))
            pattern = data.get("pattern", PATTERN_GOOD)
            if pattern not in (PATTERN_COMMANDING, PATTERN_SPOON_FEEDING, PATTERN_UNDER_TEACHING, PATTERN_GOOD):
                pattern = PATTERN_GOOD
            feedback = data.get("feedback", "") or ""
            suggestions = data.get("suggestions", [])
            if isinstance(suggestions, list):
                suggestions = [str(s) for s in suggestions[:3] if s]
            else:
                suggestions = []
            return {
                "pattern": pattern,
                "feedback": feedback[:300],
                "suggestions": suggestions,
            }
        except json.JSONDecodeError:
            pass
    return {"pattern": PATTERN_GOOD, "feedback": "", "suggestions": []}
