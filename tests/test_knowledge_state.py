"""
Unit tests for Knowledge State Engine (StateTracker).
"""
import pytest
from src.core.knowledge_state import StateTracker


@pytest.fixture
def unit_definitions():
    return [
        {"id": "var", "name": "Variables", "topic_group": "basics", "prerequisites": []},
        {"id": "print", "name": "Print", "topic_group": "io", "prerequisites": []},
        {"id": "loop", "name": "Loop", "topic_group": "control", "prerequisites": ["var"]},
    ]


def test_tracker_starts_all_unknown(unit_definitions):
    tracker = StateTracker(unit_definitions=unit_definitions, domain="python")
    assert tracker.get_learned_units() == set()
    full = tracker.get_full_state()
    assert "units" in full
    for uid, rec in full["units"].items():
        assert rec["status"] == "unknown"


def test_update_after_teaching(unit_definitions):
    tracker = StateTracker(unit_definitions=unit_definitions, domain="python")
    tracker.update_after_teaching(["var", "print"], tracker.STATUS_LEARNED)
    assert tracker.get_learned_units() == {"var", "print"}
    assert "loop" not in tracker.get_learned_units()


def test_activate_misconception(unit_definitions):
    tracker = StateTracker(unit_definitions=unit_definitions, domain="python")
    tracker.update_after_teaching(["var"], tracker.STATUS_LEARNED)
    ok = tracker.activate_misconception("var", "assign_vs_equal", set_status_to_misconception=True)
    assert ok is True
    assert tracker.get_active_misconception_ids({"var"}) == ["assign_vs_equal"]


def test_get_full_state_has_domain(unit_definitions):
    tracker = StateTracker(unit_definitions=unit_definitions, domain="python")
    full = tracker.get_full_state()
    assert full["domain"] == "python"
    assert len(full["units"]) == 3


def test_bkt_update_after_observation(unit_definitions):
    tracker = StateTracker(unit_definitions=unit_definitions, domain="python")
    tracker.update_after_teaching(["var"], tracker.STATUS_LEARNED)
    initial_p = tracker._get_p_know_raw("var")
    tracker.update_bkt_after_observation(["var"], correct=True)
    assert tracker._get_p_know_raw("var") >= initial_p
    tracker.update_bkt_after_observation(["var"], correct=False)
    assert tracker._get_p_know_raw("var") < 1.0


def test_bkt_state_and_decay(unit_definitions):
    tracker = StateTracker(unit_definitions=unit_definitions, domain="python")
    tracker.update_after_teaching(["var"], tracker.STATUS_LEARNED)
    bkt = tracker.get_bkt_state()
    assert "var" in bkt
    assert 0 <= bkt["var"] <= 1
    decayed = tracker.get_p_know_decayed("var")
    assert 0 <= decayed <= 1


def test_prerequisites_block_transit(unit_definitions):
    tracker = StateTracker(unit_definitions=unit_definitions, domain="python")
    assert tracker._prerequisites_satisfied("var") is True
    assert tracker._prerequisites_satisfied("loop") is False
    tracker.update_after_teaching(["var"], tracker.STATUS_LEARNED)
    assert tracker._prerequisites_satisfied("loop") is True


def test_merge_persisted_state(unit_definitions):
    tracker = StateTracker(unit_definitions=unit_definitions, domain="python")
    tracker.merge_persisted_state({
        "var": {"status": "learned", "bkt_p_know": 0.9},
    })
    assert tracker.get_state().get("var") == "learned"
    assert tracker._get_p_know_raw("var") == 0.9
