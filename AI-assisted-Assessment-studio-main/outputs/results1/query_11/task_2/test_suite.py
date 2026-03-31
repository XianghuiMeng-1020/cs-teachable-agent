import pytest

from solution import can_qualify

def test_all_mandatory_present():
    dish_ingredients = ['flour', 'egg', 'milk', 'sugar']
    mandatory_ingredients = ['flour', 'egg']
    assert can_qualify(dish_ingredients, mandatory_ingredients) is True

def test_some_mandatory_missing():
    dish_ingredients = ['flour', 'milk', 'sugar']
    mandatory_ingredients = ['flour', 'egg']
    assert can_qualify(dish_ingredients, mandatory_ingredients) is False

def test_no_mandatory_present():
    dish_ingredients = ['milk', 'sugar']
    mandatory_ingredients = ['flour', 'egg']
    assert can_qualify(dish_ingredients, mandatory_ingredients) is False

def test_exact_match():
    dish_ingredients = ['flour', 'egg']
    mandatory_ingredients = ['flour', 'egg']
    assert can_qualify(dish_ingredients, mandatory_ingredients) is True

def test_more_ingredients_than_needed():
    dish_ingredients = ['flour', 'egg', 'milk', 'sugar', 'butter']
    mandatory_ingredients = ['flour', 'egg', 'sugar']
    assert can_qualify(dish_ingredients, mandatory_ingredients) is True
