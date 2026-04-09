"""
Assessment grading engine.
Ported from Assessment Studio's studio-data.ts gradeStudentTask logic.
Supports three item types: parsons, dropdown, execution-trace.
"""

from __future__ import annotations

from typing import Any, Literal

ItemType = Literal["parsons", "dropdown", "execution-trace"]


def _normalize_block(text: str) -> str:
    return text.replace("\r\n", "\n").strip()


def grade_parsons(
    interaction_content: dict[str, Any],
    answer_key: dict[str, Any],
    selected_blocks: list[str],
) -> dict[str, Any]:
    code_blocks: list[str] = interaction_content.get("code_blocks", [])
    solution_order: list[int] = answer_key.get("solution_order", interaction_content.get("solution_order", []))

    canonical = [_normalize_block(code_blocks[i]) for i in solution_order if i < len(code_blocks)]
    submitted = [_normalize_block(b) for b in selected_blocks]

    expected_count = len(canonical)
    selected_count = len(submitted)
    correct_count = sum(
        1 for i, block in enumerate(canonical) if i < len(submitted) and submitted[i] == block
    )

    if selected_count == expected_count and all(
        submitted[i] == canonical[i] for i in range(expected_count)
    ):
        return _result("parsons", True, "Correct. You selected the right blocks in the right order.",
                        expected_count, selected_count, correct_count)

    if selected_count != expected_count:
        return _result("parsons", False, f"Select exactly {expected_count} blocks before submitting.",
                        expected_count, selected_count, correct_count)

    same_set = (
        set(submitted) == set(canonical) and
        all(b in submitted for b in canonical) and
        all(b in canonical for b in submitted)
    )
    if same_set:
        return _result("parsons", False, "You selected the right blocks, but the order is wrong.",
                        expected_count, selected_count, correct_count)

    return _result("parsons", False,
                    "At least one selected block is a distractor or a required block is missing.",
                    expected_count, selected_count, correct_count)


def grade_dropdown(
    interaction_content: dict[str, Any],
    answer_key: dict[str, Any],
    selected_answers: dict[str, str],
) -> dict[str, Any]:
    blanks: list[dict] = interaction_content.get("blanks", [])
    correct_answers: dict[str, str] = answer_key.get("correct_answers", {})

    blank_ids = {b.get("blank_id", "") for b in blanks}
    answered = [b for b in blanks if selected_answers.get(b.get("blank_id", ""), "").strip()]
    correct_count = sum(
        1 for b in blanks
        if selected_answers.get(b.get("blank_id", "")) == correct_answers.get(b.get("blank_id", ""))
    )
    has_unknown = any(k not in blank_ids for k in selected_answers)
    expected_count = len(blanks)
    selected_count = len(answered)
    correct = not has_unknown and correct_count == expected_count and selected_count == expected_count

    if correct:
        return _result("dropdown", True, "Correct. Every blank matches the canonical source solution.",
                        expected_count, selected_count, correct_count)
    if selected_count != expected_count:
        return _result("dropdown", False, "Answer every blank before submitting.",
                        expected_count, selected_count, correct_count)
    if has_unknown:
        return _result("dropdown", False,
                        "One or more answers were attached to an unknown blank.",
                        expected_count, selected_count, correct_count)
    if correct_count > 0:
        return _result("dropdown", False,
                        "Some blanks are correct, but at least one selected option still conflicts with the source solution.",
                        expected_count, selected_count, correct_count)
    return _result("dropdown", False,
                    "None of the selected options match the canonical source solution yet.",
                    expected_count, selected_count, correct_count)


def grade_execution_trace(
    interaction_content: dict[str, Any],
    answer_key: dict[str, Any],
    selected_answers: dict[str, str],
) -> dict[str, Any]:
    checkpoints: list[dict] = interaction_content.get("checkpoints", [])
    correct_answers: dict[str, str] = answer_key.get("correct_answers", {})

    checkpoint_ids = {cp.get("checkpoint_id", "") for cp in checkpoints}
    answered = [cp for cp in checkpoints if selected_answers.get(cp.get("checkpoint_id", ""), "").strip()]
    correct_count = sum(
        1 for cp in checkpoints
        if selected_answers.get(cp.get("checkpoint_id", "")) == correct_answers.get(cp.get("checkpoint_id", ""))
    )
    has_unknown = any(k not in checkpoint_ids for k in selected_answers)
    expected_count = len(checkpoints)
    selected_count = len(answered)
    correct = not has_unknown and correct_count == expected_count and selected_count == expected_count

    if correct:
        return _result("execution-trace", True,
                        "Correct. Every checkpoint matches the canonical execution trace.",
                        expected_count, selected_count, correct_count)
    if selected_count != expected_count:
        return _result("execution-trace", False, "Fill in every checkpoint value before submitting.",
                        expected_count, selected_count, correct_count)
    if has_unknown:
        return _result("execution-trace", False,
                        "One or more values were attached to an unknown checkpoint.",
                        expected_count, selected_count, correct_count)
    if correct_count > 0:
        return _result("execution-trace", False,
                        "Some checkpoint values are correct, but at least one traced value still differs from the canonical execution.",
                        expected_count, selected_count, correct_count)
    return _result("execution-trace", False,
                    "None of the submitted checkpoint values match the canonical execution trace yet.",
                    expected_count, selected_count, correct_count)


def grade_assessment(
    item_type: ItemType,
    interaction_content: dict[str, Any],
    answer_key: dict[str, Any],
    *,
    selected_blocks: list[str] | None = None,
    selected_answers: dict[str, str] | None = None,
) -> dict[str, Any]:
    if item_type == "parsons":
        return grade_parsons(interaction_content, answer_key, selected_blocks or [])
    if item_type == "dropdown":
        return grade_dropdown(interaction_content, answer_key, selected_answers or {})
    if item_type == "execution-trace":
        return grade_execution_trace(interaction_content, answer_key, selected_answers or {})
    raise ValueError(f"Unknown item_type: {item_type}")


def build_student_task_response(
    item: Any,
) -> dict[str, Any]:
    """Build a safe student-facing task response (no answer keys leaked)."""
    base = {
        "id": item.id,
        "item_id": item.item_id,
        "item_type": item.item_type,
        "title": item.title,
        "prompt": item.prompt,
        "theme": item.metadata_theme,
        "concepts": item.metadata_concepts or [],
        "ai_pass_rate": item.ai_pass_rate,
        "difficulty": item.difficulty,
    }

    ic = item.interaction_content or {}

    if item.item_type == "parsons":
        code_blocks = ic.get("code_blocks", [])
        distractors = ic.get("distractors", [])
        base.update({
            "required_block_count": len(code_blocks),
            "options": code_blocks,
            "distractors": distractors,
        })
    elif item.item_type == "dropdown":
        blanks = ic.get("blanks", [])
        safe_blanks = [
            {
                "blank_id": b.get("blank_id", ""),
                "placeholder": b.get("placeholder", ""),
                "options": b.get("options", []),
            }
            for b in blanks
        ]
        base.update({
            "required_blank_count": len(blanks),
            "prompt_template": ic.get("prompt_template", ""),
            "blanks": safe_blanks,
        })
    elif item.item_type == "execution-trace":
        checkpoints = ic.get("checkpoints", [])
        safe_checkpoints = [
            {
                "checkpoint_id": cp.get("checkpoint_id", ""),
                "line_number": cp.get("line_number", 0),
                "line_excerpt": cp.get("line_excerpt", ""),
                "variable_name": cp.get("variable_name", ""),
            }
            for cp in checkpoints
        ]
        base.update({
            "required_checkpoint_count": len(checkpoints),
            "function_name": ic.get("function_name", ""),
            "function_source": ic.get("function_source", ""),
            "call_expression": ic.get("call_expression", ""),
            "checkpoints": safe_checkpoints,
        })

    return base


def _result(
    item_type: str, correct: bool, feedback: str,
    expected_count: int, selected_count: int, correct_count: int,
) -> dict[str, Any]:
    next_action = _next_action(item_type, correct, expected_count, selected_count, correct_count)
    return {
        "item_type": item_type,
        "correct": correct,
        "feedback": feedback,
        "next_action": next_action,
        "expected_count": expected_count,
        "selected_count": selected_count,
        "correct_count": correct_count,
    }


def _next_action(
    item_type: str,
    correct: bool,
    expected_count: int,
    selected_count: int,
    correct_count: int,
) -> str:
    if correct:
        return "Try the next exercise or ask for a harder variant."

    if item_type == "parsons":
        if selected_count != expected_count:
            return f"Select exactly {expected_count} blocks, then check order from top to bottom."
        if correct_count > 0:
            return "Keep the same blocks and focus on reordering adjacent lines."
        return "Remove distractors first, then rebuild the core logic in small steps."

    if item_type == "dropdown":
        if selected_count != expected_count:
            return "Fill every blank before submitting again."
        if correct_count > 0:
            return "Start with one incorrect blank and justify why each option fits the context."
        return "Re-read each sentence around the blanks and eliminate obviously inconsistent options."

    if item_type == "execution-trace":
        if selected_count != expected_count:
            return "Complete every checkpoint value before the next submission."
        if correct_count > 0:
            return "Trace the code line by line and recompute only the mismatched checkpoints."
        return "Write down variable states after each line, then transfer those values to checkpoints."

    return "Review the prompt and try one focused correction before resubmitting."
