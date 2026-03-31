from program import *
import pytest
import os
from program import calculate_ingredient_costs

def setup_module(module):
    with open('test_ingredients.txt', 'w') as file:
        file.write('sugar:1.50\n')
        file.write('flour:0.75\n')
        file.write('eggs:0.50\n')
        file.write('butter:1.00\n')

    with open('empty_ingredients.txt', 'w') as file:
        pass

def teardown_module(module):
    os.remove('test_ingredients.txt')
    os.remove('empty_ingredients.txt')

def test_valid_file_full_use():
    quantities = {'sugar': 2, 'flour': 5, 'eggs': 1}
    assert calculate_ingredient_costs('test_ingredients.txt', quantities) == 9.25

def test_missing_ingredient_in_file():
    quantities = {'sugar': 2, 'flour': 2, 'honey': 1}
    assert calculate_ingredient_costs('test_ingredients.txt', quantities) == 4.50

def test_file_not_found():
    quantities = {'sugar': 2, 'flour': 5}
    assert calculate_ingredient_costs('missing_file.txt', quantities) is None

def test_empty_file():
    quantities = {'sugar': 2, 'flour': 5}
    assert calculate_ingredient_costs('empty_ingredients.txt', quantities) == 0

def test_empty_quantities():
    quantities = {}
    assert calculate_ingredient_costs('test_ingredients.txt', quantities) == 0