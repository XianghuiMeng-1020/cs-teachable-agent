import pytest
from solution import FleetManager

def test_add_ship_success():
    fm = FleetManager()
    fm.add_ship("Enterprise", 1000)
    assert "Enterprise" in fm.get_fleet_summary()


def test_add_ship_duplicate_error():
    fm = FleetManager()
    fm.add_ship("Enterprise", 1000)
    with pytest.raises(ValueError):
        fm.add_ship("Enterprise", 1200)


def test_record_mission_success():
    fm = FleetManager()
    fm.add_ship("Falcon", 900)
    fm.record_mission("Falcon", "Mars Exploration")
    assert "Mars Exploration" in fm.get_missions("Falcon")


def test_record_mission_no_ship_error():
    fm = FleetManager()
    with pytest.raises(KeyError):
        fm.record_mission("Voyager", "Jupiter Flyby")


def test_get_fleet_summary_structure():
    fm = FleetManager()
    fm.add_ship("Apollo", 800)
    fm.record_mission("Apollo", "Moon Landing")
    summary = fm.get_fleet_summary()
    assert summary == {"Apollo": {"max_speed": 800, "missions": ["Moon Landing"]}}


def test_get_missions_no_ship():
    fm = FleetManager()
    missions = fm.get_missions("NonExistent")
    assert missions == []
