import os
import pytest
from solution import KitchenInventory

filename = 'test_inventory.txt'

# Setup function creates a test file with initial data

def setup_module(module):
    with open(filename, 'w') as f:
        f.write('sugar:10\n')
        f.write('flour:5\n')
        f.write('butter:2\n')

# Teardown function removes the test file

def teardown_module(module):
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def inventory():
    inv = KitchenInventory(filename)
    inv.load_inventory()
    return inv

# Tests loading the inventory from a file

def test_load_inventory(inventory):
    assert inventory.check_availability('sugar') == True
    assert inventory.check_availability('flour') == True
    assert inventory.check_availability('butter') == True
    assert inventory.check_availability('milk') == False

# Tests checking availability of ingredients

def test_check_availability(inventory):
    assert inventory.check_availability('sugar') == True
    assert inventory.check_availability('olive oil') == False

# Tests adding ingredients to the inventory

def test_add_ingredient(inventory):
    inventory.add_ingredient('sugar', 5)
    assert inventory.check_availability('sugar') == True
    inventory.add_ingredient('olive oil', 3)
    assert inventory.check_availability('olive oil') == True

# Tests saving the inventory to a file

def test_save_inventory():
    inv = KitchenInventory(filename)
    inv.load_inventory()
    inv.add_ingredient('salt', 2)
    inv.save_inventory()
    with open(filename, 'r') as file:
        data = file.read()
        assert 'salt:2' in data

# Tests handling non-existing file

def test_non_existing_file_handling():
    temp_filename = 'non_existing_inventory.txt'
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
    inv = KitchenInventory(temp_filename)
    inv.load_inventory() # Should not raise any exception
    assert inv.check_availability('sugar') == False
    inv.add_ingredient('sugar', 5)
    inv.save_inventory()
    with open(temp_filename, 'r') as file:
        data = file.read()
    assert 'sugar:5' in data
    os.remove(temp_filename)