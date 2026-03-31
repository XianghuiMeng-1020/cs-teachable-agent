from solution_program import *
import pytest
from solution_program import Spaceship

def test_add_and_total_weight():
    ship = Spaceship("Galactic Falcon", 500)
    ship.add_item("Laser Cannon", "Weapon", 60)
    assert ship.total_weight() == 60
    ship.add_item("Shield Generator", "Defense", 80)
    assert ship.total_weight() == 140


def test_item_update():
    ship = Spaceship("Galactic Falcon", 500)
    ship.add_item("Laser Cannon", "Weapon", 60)
    ship.add_item("Laser Cannon", "Weapon Upgraded", 70)
    assert ship.list_items() == [("Laser Cannon", "Weapon Upgraded", 70)]
    assert ship.total_weight() == 70


def test_insufficient_capacity():
    ship = Spaceship("Galactic Falcon", 100)
    ship.add_item("Laser Cannon", "Weapon", 60)
    with pytest.raises(Exception) as e:
        ship.add_item("Battle Armor", "Defense", 50)
    assert str(e.value) == "Insufficient capacity"


def test_item_removal():
    ship = Spaceship("Galactic Falcon", 500)
    ship.add_item("Laser Cannon", "Weapon", 60)
    ship.remove_item("Laser Cannon")
    assert ship.total_weight() == 0
    with pytest.raises(Exception) as e:
        ship.remove_item("Laser Cannon")
    assert str(e.value) == "Item not found"


def test_list_items():
    ship = Spaceship("Galactic Falcon", 500)
    ship.add_item("Laser Cannon", "Weapon", 60)
    ship.add_item("Shield Generator", "Defense", 80)
    items = ship.list_items()
    expected_items = [
        ("Laser Cannon", "Weapon", 60),
        ("Shield Generator", "Defense", 80)
    ]
    assert items == expected_items
