from program import *
import pytest
from program import SpaceshipFleet, Spaceship

@pytest.fixture
def fleet():
    return SpaceshipFleet()

# Test adding spaceships and handling duplicates

def test_add_spaceship(fleet):
    fleet.add_spaceship("Andromeda", 500, 80)
    fleet.add_spaceship("Falcon", 600, 90)
    assert len(fleet.ships) == 2
    with pytest.raises(ValueError):
        fleet.add_spaceship("Andromeda", 700, 70)

# Test removing a spaceship and handling non-existent spaceship

def test_remove_spaceship(fleet):
    fleet.add_spaceship("Andromeda", 500, 80)
    fleet.remove_spaceship("Andromeda")
    assert len(fleet.ships) == 0
    with pytest.raises(KeyError):
        fleet.remove_spaceship("Andromeda")

# Test getting the fastest spaceship

def test_get_fastest_spaceship(fleet):
    fleet.add_spaceship("Andromeda", 500, 80)
    fleet.add_spaceship("Zephyr", 550, 60)
    fleet.add_spaceship("Falcon", 600, 90)
    assert fleet.get_fastest_spaceship() == "Falcon"
    fleet.remove_spaceship("Falcon")
    assert fleet.get_fastest_spaceship() == "Zephyr"
    fleet.remove_spaceship("Andromeda")
    fleet.remove_spaceship("Zephyr")
    with pytest.raises(RuntimeError):
        fleet.get_fastest_spaceship()

# Test getting fuel status

def test_get_fuel_status(fleet):
    fleet.add_spaceship("Andromeda", 500, 80)
    fleet.add_spaceship("Zephyr", 550, 60)
    fuel_status = fleet.get_fuel_status()
    expected = [
        {'name': 'Andromeda', 'fuel': 80},
        {'name': 'Zephyr', 'fuel': 60}
    ]
    assert fuel_status == expected
