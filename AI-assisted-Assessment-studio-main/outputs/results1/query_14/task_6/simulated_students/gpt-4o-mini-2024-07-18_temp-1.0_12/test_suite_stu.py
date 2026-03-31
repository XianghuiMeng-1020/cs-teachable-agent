from solution_program import *
import pytest
from solution_program import recipe_summary

# Test for basic functionality
def test_single_ingredient():
    recipe = "flour: 200 grams"
    expected = {"flour": {"quantity": "200", "unit": "grams"}}
    assert recipe_summary(recipe) == expected

# Test multiple ingredients
def test_multiple_ingredients():
    recipe = "flour: 200 grams\nsugar: 100 grams\nbutter: 50 grams"
    expected = {
        "flour": {"quantity": "200", "unit": "grams"},
        "sugar": {"quantity": "100", "unit": "grams"},
        "butter": {"quantity": "50", "unit": "grams"}
    }
    assert recipe_summary(recipe) == expected

# Test different units
def test_different_units():
    recipe = "milk: 1 liter\neggs: 2 units"
    expected = {
        "milk": {"quantity": "1", "unit": "liter"},
        "eggs": {"quantity": "2", "unit": "units"}
    }
    assert recipe_summary(recipe) == expected

# Test empty string
def test_empty_string():
    recipe = ""
    expected = {}
    assert recipe_summary(recipe) == expected

# Test complex input
def test_complex_input():
    recipe = "vegetables: 500 grams\nwater: 2 liters\nmeat: 1 kilogram"
    expected = {
        "vegetables": {"quantity": "500", "unit": "grams"},
        "water": {"quantity": "2", "unit": "liters"},
        "meat": {"quantity": "1", "unit": "kilogram"}
    }
    assert recipe_summary(recipe) == expected
