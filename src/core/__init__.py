"""Core engine layer: knowledge state, teaching interpreter, dialogue, task, attempt, evaluator, trace, orchestrator."""

from src.core.knowledge_state import StateTracker
from src.core.teaching_events import make_teaching_event, apply_teaching_event
from src.core.task_engine import (
    load_problems,
    select_problem,
    get_eligible_problem_ids,
    get_ineligible_reasons,
)
from src.core.dialogue_engine import get_ta_learner_response
from src.core.attempt_engine import get_ta_code_attempt
from src.core.evaluator import (
    evaluate_attempt,
    mastery_summary,
    build_mastery_report,
    record_attempt_to_state,
)
from src.core.trace import (
    record_teaching_event,
    record_knowledge_state_update,
    record_learner_dialogue,
    record_task_selection,
    record_ta_attempt,
    record_evaluation_result,
    record_mastery_update,
    get_trace_events,
    clear_trace,
)
from src.core.misconception_engine import (
    activate_misconception_for_unit,
    apply_correction,
    add_relearning_evidence_from_teaching,
)
from src.core.correction_events import make_correction_event
from src.core.teaching_interpreter import interpret_teaching
from src.core.orchestrator import (
    run_teaching_and_test,
    run_correction,
    run_relearning_step,
    run_test_only,
)

__all__ = [
    "StateTracker",
    "make_teaching_event",
    "apply_teaching_event",
    "load_problems",
    "select_problem",
    "get_eligible_problem_ids",
    "get_ineligible_reasons",
    "get_ta_learner_response",
    "get_ta_code_attempt",
    "evaluate_attempt",
    "mastery_summary",
    "build_mastery_report",
    "record_attempt_to_state",
    "record_teaching_event",
    "record_knowledge_state_update",
    "record_learner_dialogue",
    "record_task_selection",
    "record_ta_attempt",
    "record_evaluation_result",
    "record_mastery_update",
    "get_trace_events",
    "clear_trace",
    "activate_misconception_for_unit",
    "apply_correction",
    "add_relearning_evidence_from_teaching",
    "make_correction_event",
    "interpret_teaching",
    "run_teaching_and_test",
    "run_correction",
    "run_relearning_step",
    "run_test_only",
]
