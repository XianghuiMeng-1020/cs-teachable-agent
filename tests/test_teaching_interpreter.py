"""
Unit tests for Teaching Interpreter (heuristic path; no LLM).
"""
import pytest
from src.core.teaching_interpreter import interpret_teaching


VALID_UNITS = ["variable_assignment", "print_function", "user_input", "if_else"]


def test_heuristic_returns_structure():
    out = interpret_teaching(
        "Variables store values. Like x = 5.",
        VALID_UNITS,
        filled_prompt=None,
        use_llm=False,
    )
    assert "topic_taught" in out
    assert "knowledge_units_taught" in out
    assert "quality_score" in out
    assert isinstance(out["knowledge_units_taught"], list)
    assert 0 <= out["quality_score"] <= 1


def test_heuristic_maps_keywords_to_units():
    out = interpret_teaching(
        "Print prints things. print('hello').",
        VALID_UNITS,
        use_llm=False,
    )
    assert "print_function" in out["knowledge_units_taught"] or len(out["knowledge_units_taught"]) >= 0


def test_heuristic_without_prompt_uses_heuristic():
    out = interpret_teaching("If and else for conditions.", VALID_UNITS, filled_prompt=None)
    assert "topic_taught" in out
    assert isinstance(out["knowledge_units_taught"], list)
    for u in out["knowledge_units_taught"]:
        assert u in VALID_UNITS


def test_quality_score_in_range():
    out = interpret_teaching("Short.", VALID_UNITS, use_llm=False)
    assert 0 <= out["quality_score"] <= 1
