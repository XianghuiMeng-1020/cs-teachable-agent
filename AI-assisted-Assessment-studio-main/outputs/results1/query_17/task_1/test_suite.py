import pytest
from solution import SpaceCargo

def setup_module(module):
    module.ship_cargo = SpaceCargo()
    ship_cargo.add_item("Oxygen", 50)
    ship_cargo.add_item("Food", 20)


def teardown_module(module):
    del module.ship_cargo


def test_add_item_new():
    cargo = SpaceCargo()
    cargo.add_item("Fuel", 100)
    assert cargo.get_item_quantity("Fuel") == 100


def test_add_item_existing():
    ship_cargo.add_item("Oxygen", 30)
    assert ship_cargo.get_item_quantity("Oxygen") == 80


def test_add_item_invalid_quantity():
    with pytest.raises(ValueError):
        ship_cargo.add_item("Helium", -10)


def test_remove_item_sufficient():
    ship_cargo.remove_item("Food", 10)
    assert ship_cargo.get_item_quantity("Food") == 10


def test_remove_item_insufficient():
    with pytest.raises(KeyError):
        ship_cargo.remove_item("Food", 30)


def test_remove_item_nonexistent():
    with pytest.raises(KeyError):
        ship_cargo.remove_item("Water", 10)


def test_get_item_quantity_nonexistent():
    assert ship_cargo.get_item_quantity("Water") == 0


def test_list_items():
    expected_items = sorted(["Food", "Oxygen"])
    assert ship_cargo.list_items() == expected_items