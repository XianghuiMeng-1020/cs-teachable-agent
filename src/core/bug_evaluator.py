"""
Evaluate whether a student correctly identified a bug in a buggy-code problem.
Returns code_modification payload if the identification is correct.
"""

from __future__ import annotations

import json
import re
from typing import Any

from src.llm.client import llm_completion


def evaluate_bug_identification(
    student_input: str,
    problem: dict,
    conversation_history: list[dict] | None = None,
) -> dict[str, Any]:
    """
    Evaluate if the student correctly identified the bug in a buggy-code problem.
    Returns:
        {
            "correct": bool,
            "confidence": float (0-1),
            "code_modification": {...} | None,
            "feedback": str,
            "hint_level": int  (0 = no hint needed, 1-3 = progressive hints)
        }
    """
    code = problem.get("code", "")
    bug_lines = problem.get("bug_lines", [])
    bug_explanation = problem.get("bug_explanation", "")
    correct_code = problem.get("correct_code", "")

    if not code or not student_input:
        return {
            "correct": False,
            "confidence": 0.0,
            "code_modification": None,
            "feedback": "Please describe what you think is wrong with the code.",
            "hint_level": 0,
        }

    prompt = f"""You are evaluating whether a student correctly identified a bug in Python code.

## Buggy Code:
```python
{code}
```

## Known Bug Info:
- Bug lines: {bug_lines}
- Bug explanation: {bug_explanation}

## Student's Analysis:
"{student_input}"

## Recent conversation (for context):
{_format_history(conversation_history)}

## Task:
Determine if the student correctly identified:
1) Which line(s) have the bug (they don't need exact line numbers, just correct identification)
2) Why it's a bug (the root cause)

Reply with JSON only:
{{
  "correct": true/false,
  "confidence": 0.0-1.0,
  "partial_credit": true/false,
  "reasoning": "brief explanation of your assessment"
}}"""

    result = llm_completion(prompt, max_tokens=200, temperature=0.1)
    parsed = _parse_json(result)

    correct = parsed.get("correct", False)
    confidence = min(1.0, max(0.0, float(parsed.get("confidence", 0.0))))
    partial = parsed.get("partial_credit", False)

    code_modification = None
    if correct and confidence >= 0.5 and bug_lines and correct_code:
        original_lines = code.split("\n")
        fixed_lines = correct_code.split("\n")
        for line_num in bug_lines:
            idx = line_num - 1
            if idx < len(original_lines) and idx < len(fixed_lines):
                code_modification = {
                    "line_number": line_num,
                    "old_code": original_lines[idx],
                    "new_code": fixed_lines[idx],
                    "explanation": bug_explanation,
                }
                break

    feedback = ""
    if correct:
        feedback = "Excellent identification! You correctly found the bug."
    elif partial:
        feedback = "You're on the right track but haven't fully explained the root cause."
    else:
        feedback = parsed.get("reasoning", "Try looking more carefully at the code.")

    return {
        "correct": correct,
        "confidence": confidence,
        "code_modification": code_modification,
        "feedback": feedback,
        "hint_level": 0 if correct else (1 if partial else 0),
    }


def get_progressive_hint(
    problem: dict,
    hint_level: int,
    conversation_history: list[dict] | None = None,
) -> str | None:
    """
    Generate a progressive hint based on the current hint level.
    Returns None if no hint needed (level 0).
    """
    if hint_level <= 0:
        return None

    code = problem.get("code", "")
    bug_lines = problem.get("bug_lines", [])
    bug_explanation = problem.get("bug_explanation", "")
    knowledge_units = problem.get("knowledge_units_tested", [])

    if hint_level == 1:
        if bug_lines:
            region = f"around line{'s' if len(bug_lines) > 1 else ''} {', '.join(str(l) for l in bug_lines)}"
            return f"Take a closer look at the code {region}. What happens when that line executes?"
        return "Read through the code line by line. Think about what each line does."

    if hint_level == 2:
        concepts = ", ".join(knowledge_units) if knowledge_units else "the main concept"
        return f"This bug is related to {concepts}. Think about what could go wrong with that concept in this context."

    if hint_level >= 3:
        return f"Here's a strong hint: {bug_explanation[:100]}{'...' if len(bug_explanation) > 100 else ''}"

    return None


def compute_hint_level(
    incorrect_attempts: int,
) -> int:
    """Map number of incorrect attempts to hint level."""
    if incorrect_attempts >= 6:
        return 3
    if incorrect_attempts >= 4:
        return 2
    if incorrect_attempts >= 2:
        return 1
    return 0


def _format_history(history: list[dict] | None) -> str:
    if not history:
        return "(no prior conversation)"
    lines = []
    for msg in history[-4:]:
        role = msg.get("role", "?")
        content = (msg.get("content") or "")[:150]
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def _parse_json(text: str | None) -> dict:
    if not text:
        return {}
    match = re.search(r"\{[\s\S]*\}", text.strip())
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {}
