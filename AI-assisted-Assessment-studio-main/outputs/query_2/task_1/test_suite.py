import pytest
import os
from solution import find_recipes_with_ingredient

RECIPE_FILE = "recipes.txt"

CONTENT = """Chocolate Cake
Flour
Sugar
Cocoa
Eggs
Milk

Caesar Salad
Lettuce
Croutons
Parmesan Cheese
Caesar Dressing

Spaghetti Bolognese
Spaghetti
Ground Beef
Tomato Sauce
Garlic
"""


def setup_module(module):
    with open(RECIPE_FILE, "w") as f:
        f.write(CONTENT)

def teardown_module(module):
    os.remove(RECIPE_FILE)


def test_find_recipes_with_ingredient_simple_case():
    result = find_recipes_with_ingredient(RECIPE_FILE, "Garlic")
    assert result == ["Spaghetti Bolognese"]


def test_find_recipes_with_ingredient_case_sensitivity():
    result = find_recipes_with_ingredient(RECIPE_FILE, "garlic")
    assert result == []


def test_find_recipes_with_ingredient_no_result():
    result = find_recipes_with_ingredient(RECIPE_FILE, "Olive Oil")
    assert result == []


def test_find_recipes_multiple_ingredient_usages():
    result = find_recipes_with_ingredient(RECIPE_FILE, "Sugar")
    assert result == ["Chocolate Cake"]


def test_find_recipes_with_ingredient_empty_ingredient():
    result = find_recipes_with_ingredient(RECIPE_FILE, "")
    assert result == []  
