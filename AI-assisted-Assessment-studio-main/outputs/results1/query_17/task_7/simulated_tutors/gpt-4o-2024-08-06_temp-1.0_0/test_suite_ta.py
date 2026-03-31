from program import *
import pytest
from galaxy_explorer import Spaceship, Fleet


def test_spaceship_creation():
    ship = Spaceship("Voyager", 100, ["Mars", "Jupiter"])
    assert ship.name == "Voyager"
    assert ship.fuel_level == 100
    assert ship.destinations == ["Mars", "Jupiter"]


def test_add_fuel():
    ship = Spaceship("Odyssey", 40, [])
    ship.add_fuel(20)
    assert ship.fuel_level == 60


def test_travel_success():
    ship = Spaceship("Endeavour", 100, ["Saturn", "Titan"])
    ship.travel("Saturn")
    assert ship.fuel_level == 90
    assert ship.destinations == ["Titan"]


def test_travel_insufficient_fuel():
    ship = Spaceship("Curiosity", 5, ["Venus"])
    with pytest.raises(Exception):
        ship.travel("Venus")


def test_diagnostic():
    ship1 = Spaceship("Pioneer", 60, [])
    ship2 = Spaceship("Explorer", 45, [])
    fleet = Fleet()
    fleet.add_spaceship(ship1)
    fleet.add_spaceship(ship2)
    result = fleet.diagnostic()
    assert result == {"Pioneer": "PASS", "Explorer": "FAIL"}