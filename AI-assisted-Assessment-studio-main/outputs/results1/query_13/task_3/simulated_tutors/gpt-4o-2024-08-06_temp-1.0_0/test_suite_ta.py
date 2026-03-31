from program import *
import pytest
import os
from program import cook_recipe

def test_enough_ingredients():
    ingredients = [('flour', 200), ('sugar', 100)]
    available = {'flour': 300, 'sugar': 100}
    result = cook_recipe(ingredients, available)
    assert result == ['flour: Enough', 'sugar: Enough']

def test_not_enough_ingredients():
    ingredients = [('flour', 200), ('sugar', 150)]
    available = {'flour': 150, 'sugar': 100}
    result = cook_recipe(ingredients, available)
    assert result == ['flour: Not Enough, 50 grams more needed', 'sugar: Not Enough, 50 grams more needed']

def test_some_missing_ingredients():
    ingredients = [('flour', 200), ('sugar', 100), ('eggs', 2)]
    available = {'flour': 250, 'sugar': 100}
    result = cook_recipe(ingredients, available)
    assert result == ['flour: Enough', 'sugar: Enough', 'eggs: Missing']

def test_all_missing_ingredients():
    ingredients = [('butter', 50), ('milk', 200)]
    available = {'flour': 200, 'sugar': 100}
    result = cook_recipe(ingredients, available)
    assert result == ['butter: Missing', 'milk: Missing']

def test_catch_general_exceptions():
    ingredients = [('flour', '200g'), ('sugar', 100)]
    available = {'flour': 300, 'sugar': 100}
    result = cook_recipe(ingredients, available)
    assert result == 'Error'