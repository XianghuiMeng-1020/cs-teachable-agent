import pytest
from solution import Spaceship


def test_create_spaceship_with_captain():
    ship = Spaceship(name="Endeavor", captain="James T.")
    assert ship.name == "Endeavor"
    assert ship.captain == "James T."
    assert ship.missions == []


def test_create_spaceship_without_captain():
    ship = Spaceship(name="Discovery")
    assert ship.name == "Discovery"
    assert ship.captain == "Unknown"
    assert ship.missions == []


def test_add_valid_missions():
    ship = Spaceship(name="Voyager")
    ship.add_mission("Reconnaissance")
    ship.add_mission("Transport")
    ship.add_mission("Combat")
    assert ship.missions == ["Reconnaissance", "Transport", "Combat"]
    summary = ship.get_missions_summary()
    assert summary == {"Reconnaissance": 1, "Transport": 1, "Combat": 1}


def test_add_invalid_mission_raises_exception():
    ship = Spaceship(name="Enterprise")
    with pytest.raises(ValueError) as excinfo:
        ship.add_mission("Exploration")
    assert "Invalid mission type" in str(excinfo.value)


def test_mission_summary():
    ship = Spaceship(name="Atlantis")
    ship.add_mission("Reconnaissance")
    ship.add_mission("Reconnaissance")
    ship.add_mission("Combat")
    summary = ship.get_missions_summary()
    assert summary == {"Reconnaissance": 2, "Transport": 0, "Combat": 1}