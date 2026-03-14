"""
Unit tests for Misconception Engine (activate, correct, relearn).
"""
import pytest
from src.core.knowledge_state import StateTracker
from src.core.misconception_engine import (
    activate_misconception_for_unit,
    apply_correction,
    add_relearning_evidence_from_teaching,
)


@pytest.fixture
def tracker():
    units = [
        {"id": "var", "name": "Variables", "topic_group": "b", "prerequisites": []},
        {"id": "cond", "name": "Conditionals", "topic_group": "c", "prerequisites": ["var"]},
    ]
    t = StateTracker(unit_definitions=units, domain="python")
    t.update_after_teaching(["var", "cond"], t.STATUS_LEARNED)
    return t


def test_activate_misconception_for_unit(tracker):
    ok = activate_misconception_for_unit(tracker, "cond", "assign_vs_equal")
    assert ok is True
    assert "assign_vs_equal" in tracker.get_active_misconception_ids({"cond"})


def test_activate_invalid_unit(tracker):
    ok = activate_misconception_for_unit(tracker, "nonexistent", "assign_vs_equal")
    assert ok is False


def test_apply_correction(tracker):
    activate_misconception_for_unit(tracker, "cond", "assign_vs_equal")
    ok = apply_correction(tracker, "cond", "assign_vs_equal")
    assert ok is True
    assert tracker.get_active_misconception_ids({"cond"}) == []
    rec = tracker.get_unit_record("cond")
    assert rec and rec.get("status") == tracker.STATUS_CORRECTED


def test_apply_correction_nonexistent_unit(tracker):
    ok = apply_correction(tracker, "nonexistent", "assign_vs_equal")
    assert ok is False
