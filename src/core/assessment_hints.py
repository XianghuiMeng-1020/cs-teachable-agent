"""
AI hint generation for structured assessments.
Ported from Assessment Studio's openai-hint.ts and hint-service.ts.
Uses the existing src/llm/ unified call layer.

IMPORTANT: Hints are strictly constrained per level to prevent answer leakage.
"""

from __future__ import annotations

import json
import logging
import re
import uuid
from typing import Any, Literal

from src.llm.client import llm_completion

logger = logging.getLogger(__name__)

HintType = Literal["understand", "next-step", "check-one-issue"]
HintLevel = Literal[1, 2, 3]


# ── Per-level scope constraints ──────────────────────────────────────
# These definitions are injected into the system prompt AND used for
# post-generation validation to catch any answer leakage.

LEVEL_SCOPE = {
    1: {
        "label": "Conceptual only",
        "allowed": [
            "Restate what the task is asking in your own words",
            "Name the broad programming concept involved (e.g., 'loop logic', 'parameter passing')",
            "Remind the student of a general strategy ('trace through line by line')",
        ],
        "forbidden": [
            "Naming ANY specific block, blank, or checkpoint by position or content",
            "Referencing any concrete code element from the task",
            "Mentioning how many items are correct or wrong",
            "Suggesting which direction to move blocks, which option to select, or what value to enter",
        ],
    },
    2: {
        "label": "Regional pointer",
        "allowed": [
            "Point to a GENERAL area ('look at the middle section', 'check around the return statement')",
            "Describe the TYPE of error without locating it exactly ('one variable name seems off')",
            "Suggest a thinking approach ('compare the loop condition to the expected output')",
        ],
        "forbidden": [
            "Giving the exact position number of any block",
            "Naming the specific dropdown option to select",
            "Revealing the correct value for any checkpoint",
            "Stating which specific block is in the wrong place",
            "Providing code snippets that are part of the answer",
        ],
    },
    3: {
        "label": "Targeted nudge",
        "allowed": [
            "Name ONE specific element to inspect (e.g., 'look at checkpoint #3' or 'the block that starts with def...')",
            "Describe what is wrong with that ONE element conceptually ('the order of these two operations matters')",
            "Suggest a specific check ('what does range() return when given these arguments?')",
        ],
        "forbidden": [
            "Revealing the CORRECT value, position, or option for any element",
            "Giving the final block order or any portion of it",
            "Stating the exact dropdown choice to pick",
            "Providing the exact checkpoint answer",
            "Writing any code that directly solves the problem",
            "Telling the student to 'swap block X and Y' (reveals the ordering)",
        ],
    },
}


def _build_system_prompt(hint_type: HintType, level: HintLevel) -> str:
    """Build a strict system prompt with per-level constraints."""
    scope = LEVEL_SCOPE[level]

    lines = [
        "You are a concise, Socratic programming coach inside a structured student assessment UI.",
        "Your ONLY job is to give the student a small pedagogical nudge — NEVER the answer.",
        "",
        "═══ ABSOLUTE RULES (violating any one = failure) ═══",
        "",
        "1. NEVER reveal the correct answer, correct order, correct option, or correct value — not even partially.",
        "2. NEVER output code that solves or partially solves the problem.",
        "3. NEVER say 'the answer is', 'you should pick', 'the correct block is', 'swap X and Y',",
        "   'move X before Y', 'select option X', or 'the value is X'.",
        "4. NEVER give the final block sequence, even disguised as an 'example'.",
        "5. If the task has distractors (wrong blocks), NEVER identify which blocks are distractors.",
        "6. Keep the body to at most 2 sentences and under 60 words.",
        "7. Prefer Socratic questions ('What would happen if…?') over declarative statements.",
        "8. If the student already has correct progress, acknowledge it briefly and focus on what remains.",
        "",
        f"═══ CURRENT LEVEL: {level} — {scope['label']} ═══",
        "",
        "ALLOWED at this level:",
    ]
    for a in scope["allowed"]:
        lines.append(f"  ✓ {a}")

    lines.append("")
    lines.append("FORBIDDEN at this level:")
    for f in scope["forbidden"]:
        lines.append(f"  ✗ {f}")

    lines.append("")
    lines.append(f"═══ HINT TYPE: {hint_type} ═══")
    lines.append("")

    if hint_type == "understand":
        lines.append("Goal: Help the student understand WHAT the task is asking, not HOW to solve it.")
        lines.append("Frame the task in plain language. Do not suggest actions.")
    elif hint_type == "next-step":
        lines.append("Goal: Suggest the student's NEXT concrete thinking step — not the answer step.")
        lines.append("E.g., 'Try tracing what happens at line 5' — NOT 'put X at position 3'.")
    elif hint_type == "check-one-issue":
        lines.append("Goal: Point the student toward ONE potential issue to examine.")
        lines.append("Describe the symptom or concept, not the fix.")

    lines.extend([
        "",
        'Respond with valid JSON matching this schema:',
        '{"title": string, "body": string, "target": null | {"kind": "blank"|"checkpoint"|"block"|"task", "id": string, "label": string}, "escalationAvailable": boolean}',
    ])

    return "\n".join(lines)


# ── Answer leakage detector ──────────────────────────────────────────

_LEAKAGE_PATTERNS = [
    r"(?i)\bthe\s+(correct|right|proper)\s+(answer|value|option|order|sequence)\s+is\b",
    r"(?i)\byou\s+should\s+(pick|choose|select|enter|type|use)\b",
    r"(?i)\bswap\s+block\b",
    r"(?i)\bmove\s+.*\s+(before|after|to position)\b",
    r"(?i)\bthe\s+answer\s+is\b",
    r"(?i)\bplace\s+.*\s+at\s+(position|step)\s+\d",
    r"(?i)\bselect\s+['\"].*['\"]\s+for\s+blank\b",
    r"(?i)\bthe\s+value\s+(of|for).*\s+is\s+\d",
    r"(?i)\bcorrect\s+order\s+(is|would be)\b",
]


def _hint_leaks_answer(body: str) -> bool:
    """Return True if the hint body likely contains an answer."""
    for pattern in _LEAKAGE_PATTERNS:
        if re.search(pattern, body):
            return True
    return False


def _sanitize_hint(body: str, level: HintLevel) -> str:
    """If a hint leaks an answer, replace it with a safe fallback."""
    if not _hint_leaks_answer(body):
        return body

    logger.warning("Hint body failed leakage check (level %d): %s", level, body[:120])
    fallbacks = {
        1: "Take a step back and re-read the task description. What is the core concept being tested here?",
        2: "Look carefully at your current progress. Is there a section that doesn't match the expected behavior?",
        3: "Focus on the element that feels most uncertain. Trace through its logic step by step — does it do what you expect?",
    }
    return fallbacks.get(level, fallbacks[1])


# ── Helpers ───────────────────────────────────────────────────────────

def _clip(text: str, max_len: int) -> str:
    normalized = " ".join(text.split()).strip()
    if len(normalized) <= max_len:
        return normalized
    return normalized[: max_len - 3] + "..."


def _build_task_snapshot(task: dict[str, Any]) -> dict[str, Any]:
    item_type = task.get("item_type", "")

    if item_type == "parsons":
        options = task.get("options", [])
        return {
            "itemType": item_type,
            "title": task.get("title", ""),
            "prompt": _clip(task.get("prompt", ""), 900),
            "theme": task.get("theme"),
            "concepts": task.get("concepts", []),
            "requiredBlockCount": task.get("required_block_count", 0),
            "optionPool": [{"blockId": f"block_{i+1}", "text": _clip(o, 180)} for i, o in enumerate(options)],
        }

    if item_type == "dropdown":
        blanks = task.get("blanks", [])
        return {
            "itemType": item_type,
            "title": task.get("title", ""),
            "prompt": _clip(task.get("prompt", ""), 900),
            "theme": task.get("theme"),
            "concepts": task.get("concepts", []),
            "promptTemplate": _clip(task.get("prompt_template", ""), 1200),
            "blanks": [
                {"blankId": b["blank_id"], "placeholder": b["placeholder"], "options": [_clip(o, 120) for o in b.get("options", [])]}
                for b in blanks
            ],
        }

    checkpoints = task.get("checkpoints", [])
    return {
        "itemType": item_type,
        "title": task.get("title", ""),
        "prompt": _clip(task.get("prompt", ""), 900),
        "theme": task.get("theme"),
        "concepts": task.get("concepts", []),
        "functionName": task.get("function_name", ""),
        "callExpression": _clip(task.get("call_expression", ""), 240),
        "functionSource": _clip(task.get("function_source", ""), 1800),
        "checkpoints": [
            {"checkpointId": cp["checkpoint_id"], "lineNumber": cp["line_number"],
             "lineExcerpt": _clip(cp["line_excerpt"], 180), "variableName": cp["variable_name"]}
            for cp in checkpoints
        ],
    }


def _build_submission_snapshot(
    task: dict[str, Any],
    selected_blocks: list[str] | None,
    selected_answers: dict[str, str] | None,
) -> dict[str, Any]:
    item_type = task.get("item_type", "")

    if item_type == "parsons":
        blocks = selected_blocks or []
        required = task.get("required_block_count", 0)
        return {
            "itemType": item_type,
            "selectedCount": len(blocks),
            "requiredCount": required,
            "selectedBlocks": [{"position": i + 1, "text": _clip(b, 180)} for i, b in enumerate(blocks)],
            "unplacedCount": max(required - len(blocks), 0),
        }

    answers = selected_answers or {}

    if item_type == "dropdown":
        blanks = task.get("blanks", [])
        return {
            "itemType": item_type,
            "answeredCount": sum(1 for b in blanks if answers.get(b["blank_id"], "").strip()),
            "requiredCount": task.get("required_blank_count", 0),
            "selectedAnswers": [
                {"blankId": b["blank_id"], "placeholder": b["placeholder"],
                 "selected": answers.get(b["blank_id"]) or None}
                for b in blanks
            ],
        }

    checkpoints = task.get("checkpoints", [])
    return {
        "itemType": item_type,
        "answeredCount": sum(1 for cp in checkpoints if answers.get(cp["checkpoint_id"], "").strip()),
        "requiredCount": task.get("required_checkpoint_count", 0),
        "selectedAnswers": [
            {"checkpointId": cp["checkpoint_id"], "variableName": cp["variable_name"],
             "lineNumber": cp["line_number"], "selected": answers.get(cp["checkpoint_id"]) or None}
            for cp in checkpoints
        ],
    }


# ── Main entry point ─────────────────────────────────────────────────

def generate_assessment_hint(
    task: dict[str, Any],
    hint_type: HintType,
    level: HintLevel,
    *,
    selected_blocks: list[str] | None = None,
    selected_answers: dict[str, str] | None = None,
    last_feedback: dict[str, Any] | None = None,
    reflection: str | None = None,
    progress_summary: str | None = None,
    attempt_number: int | None = None,
) -> dict[str, Any]:
    """Generate an AI hint for a structured assessment item.

    Each level has strict scope constraints.  After generation, a leakage
    detector checks the output and replaces it with a safe fallback if any
    answer-revealing language is detected.
    """
    hint_id = f"hint-{uuid.uuid4()}"

    if last_feedback and last_feedback.get("correct"):
        return {
            "hint_id": hint_id,
            "hint_type": hint_type,
            "level": level,
            "title": "Already solved",
            "body": "This attempt is already correct. Use the feedback to confirm why it works, or move to the next task.",
            "target": None,
            "escalation_available": False,
            "model": "local-status",
        }

    feedback_snap = None
    if last_feedback:
        feedback_snap = {
            "correct": last_feedback.get("correct"),
            "feedback": _clip(last_feedback.get("feedback", ""), 220),
            "expectedCount": last_feedback.get("expected_count"),
            "selectedCount": last_feedback.get("selected_count"),
            "correctCount": last_feedback.get("correct_count"),
        }

    payload = {
        "requested_help": {
            "hintType": hint_type,
            "level": level,
            "reflection": _clip(reflection, 240) if reflection else None,
            "progressSummary": _clip(progress_summary, 240) if progress_summary else None,
            "attemptNumber": attempt_number,
        },
        "latest_feedback": feedback_snap,
        "task": _build_task_snapshot(task),
        "current_submission": _build_submission_snapshot(task, selected_blocks, selected_answers),
    }

    system_prompt = _build_system_prompt(hint_type, level)
    user_msg = json.dumps(payload, indent=2)

    prompt = f"{system_prompt}\n\nUser request:\n{user_msg}"

    raw = llm_completion(prompt, max_tokens=400, temperature=0.4)

    if not raw:
        fallback_prefix = {"understand": "Task frame", "next-step": "Next move", "check-one-issue": "Issue check"}.get(hint_type, "Hint")
        return {
            "hint_id": hint_id,
            "hint_type": hint_type,
            "level": level,
            "title": f"{fallback_prefix} · Level {level}",
            "body": "Hint generation is currently unavailable. Try reviewing the task prompt and your current answers.",
            "target": None,
            "escalation_available": level < 3,
            "model": "fallback",
        }

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Failed to parse hint JSON: %s", raw[:200])
        parsed = {"title": "", "body": raw, "target": None, "escalationAvailable": True}

    title = parsed.get("title", "")
    if not title or not title.strip():
        fallback_prefix = {"understand": "Task frame", "next-step": "Next move", "check-one-issue": "Issue check"}.get(hint_type, "Hint")
        title = f"{fallback_prefix} · Level {level}"
    title = _clip(title, 72)

    body = parsed.get("body", "")
    if not body or not body.strip():
        body = "Review the task prompt and your current progress for clues."
    body = _clip(body, 420)

    # Post-generation leakage check
    body = _sanitize_hint(body, level)

    target = parsed.get("target")
    if target and isinstance(target, dict):
        kind = target.get("kind")
        tid = target.get("id", "")
        if kind in ("blank", "checkpoint", "block", "task") and tid.strip():
            target = {"kind": kind, "id": _clip(tid, 80), "label": _clip(target.get("label", tid), 80)}
        else:
            target = None
    else:
        target = None

    # Level 1 should never have a specific target element
    if level == 1 and target and target.get("kind") != "task":
        target = None

    return {
        "hint_id": hint_id,
        "hint_type": hint_type,
        "level": level,
        "title": title,
        "body": body,
        "target": target,
        "escalation_available": parsed.get("escalationAvailable", level < 3),
        "model": "llm",
    }
