import pytest

from solution import recipe_value

def test_basic_recipe_value():
    assert recipe_value(['flour:2', 'sugar:1'], ['flour:0.5', 'sugar:0.8']) == 1.8

def test_recipe_with_missing_prices():
    assert recipe_value(['flour:1', 'butter:2'], ['flour:0.5']) == 0.5

def test_empty_recipe():
    assert recipe_value([], ['flour:0.5', 'sugar:0.8']) == 0.0

def test_empty_prices():
    assert recipe_value(['flour:3', 'sugar:1'], []) == 0.0

def test_recipe_and_prices_with_extra_items():
    assert recipe_value(['flour:2', 'sugar:1', 'milk:1'], ['flour:0.5', 'sugar:0.8', 'butter:0.6']) == 1.8