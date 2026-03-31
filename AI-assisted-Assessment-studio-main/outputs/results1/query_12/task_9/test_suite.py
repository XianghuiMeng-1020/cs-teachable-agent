import pytest
import os
from solution_program import find_low_cal_recipes

recipe_data = """Pasta: 300
Salad: 150
Burger: 500
Fries: 450
Soup: 200
Curry: 400
"""

recipe_empty_data = """"""

recipe_no_match = """Apple Pie: 400
Brownie: 350
Cheesecake: 250
"""

def setup_module(module):
    with open('recipe_calories.txt', 'w') as f:
        f.write(recipe_data)

    with open('recipe_empty.txt', 'w') as f:
        f.write(recipe_empty_data)

    with open('recipe_no_match.txt', 'w') as f:
        f.write(recipe_no_match)


def teardown_module(module):
    os.remove('recipe_calories.txt')
    os.remove('recipe_empty.txt')
    os.remove('recipe_no_match.txt')


def test_find_low_cal_recipes_normal_case():
    assert find_low_cal_recipes(250) == ['Salad', 'Soup']

def test_find_low_cal_recipes_no_match():
    with open('recipe_calories.txt', 'w') as f:
        f.write(recipe_no_match)
    assert find_low_cal_recipes(200) == []

def test_find_low_cal_recipes_exact_match():
    assert set(find_low_cal_recipes(400)) == set(['Salad', 'Soup', 'Pasta', 'Curry'])

def test_find_low_cal_recipes_empty_file():
    with open('recipe_calories.txt', 'w') as f:
        f.write(recipe_empty_data)
    assert find_low_cal_recipes(100) == []

def test_find_low_cal_recipes_all_match():
    assert set(find_low_cal_recipes(500)) == set(['Pasta', 'Salad', 'Burger', 'Fries', 'Soup', 'Curry'])