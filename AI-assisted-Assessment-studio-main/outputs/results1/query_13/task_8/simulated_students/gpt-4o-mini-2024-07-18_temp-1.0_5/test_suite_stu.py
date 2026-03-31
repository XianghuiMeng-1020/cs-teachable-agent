from solution_program import *
import pytest

from solution_program import calculate_ingredients

def test_multiple_ingredients():
    recipes = ["2:egg 3:flour 1:sugar", "1:egg 2:sugar 1:flour"]
    assert calculate_ingredients(recipes) == {'egg': 3, 'flour': 4, 'sugar': 3}

def test_single_recipe():
    recipes = ["4:flour 2:milk"]
    assert calculate_ingredients(recipes) == {'flour': 4, 'milk': 2}

def test_no_recipes():
    recipes = []
    assert calculate_ingredients(recipes) == {}

def test_single_ingredient_many_recipes():
    recipes = ["1:milk", "2:milk", "3:milk"]
    assert calculate_ingredients(recipes) == {'milk': 6}

def test_varied_recipes():
    recipes = ["1:egg 1:milk", "2:egg 2:milk 3:sugar", "1:flour"]
    assert calculate_ingredients(recipes) == {'egg': 3, 'milk': 3, 'sugar': 3, 'flour': 1}