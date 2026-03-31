from program import *
import pytest

from program import recipe_calculator

def test_recipe_calculator_base_case():
    recipe = {
        'flour': '2 cups',
        'sugar': '1 cup',
        'eggs': '3 units'
    }
    multiplier = 2
    expected = {
        'flour': '4 cups',
        'sugar': '2 cups',
        'eggs': '6 units'
    }
    assert recipe_calculator(recipe, multiplier) == expected


def test_recipe_calculator_fractional_result():
    recipe = {
        'milk': '3 cups',
        'butter': '1 cup'
    }
    multiplier = 1.5
    expected = {
        'milk': '5 cups',  # 4.5 rounded to 5
        'butter': '2 cups'  # 1.5 rounded to 2
    }
    assert recipe_calculator(recipe, multiplier) == expected


def test_recipe_calculator_edge_case():
    recipe = {
        'vanilla': '1 teaspoon'
    }
    multiplier = 5
    expected = {
        'vanilla': '5 teaspoons'
    }
    assert recipe_calculator(recipe, multiplier) == expected


def test_recipe_calculator_single_ingredient_zero_multiplier():
    recipe = {
        'salt': '1 pinch'
    }
    multiplier = 0.01
    expected = {
        'salt': '0 pinches'
    }
    assert recipe_calculator(recipe, multiplier) == expected


def test_recipe_calculator_large_number_of_ingredients():
    recipe = {
        'flour': '100 grams',
        'sugar': '200 grams',
        'butter': '300 grams'
    }
    multiplier = 10
    expected = {
        'flour': '1000 grams',
        'sugar': '2000 grams',
        'butter': '3000 grams'
    }
    assert recipe_calculator(recipe, multiplier) == expected
