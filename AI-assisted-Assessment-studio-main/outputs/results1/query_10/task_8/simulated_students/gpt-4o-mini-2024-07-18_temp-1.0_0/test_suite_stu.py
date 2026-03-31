from solution_program import *
import pytest
import os
from solution_program import Recipe

def setup_module(module):
    with open('recipes.txt', 'w') as f:
        f.write('Pasta\nTomato Sauce\nPasta\nCheese\nBoil pasta and mix with sauce.\n')
        f.write('Salad\nLettuce\nTomato\nOlive Oil\nMix all ingredients.\n')

def teardown_module(module):
    os.remove('recipes.txt')

def test_add_recipe():
    recipe = Recipe()
    recipe.add_recipe('Sandwich', ['Bread', 'Ham', 'Cheese', 'Lettuce'], 'Stack ingredients between bread slices.')
    result = recipe.get_recipe('Sandwich')
    assert result == {'ingredients': ['Bread', 'Ham', 'Cheese', 'Lettuce'], 'instructions': 'Stack ingredients between bread slices.'}


def test_add_existing_recipe():
    recipe = Recipe()
    with pytest.raises(Exception):
        recipe.add_recipe('Pasta', ['Pasta', 'Tomato Sauce'], 'Boil pasta and mix with sauce.')


def test_get_existing_recipe():
    recipe = Recipe()
    result = recipe.get_recipe('Salad')
    assert result['ingredients'] == ['Lettuce', 'Tomato', 'Olive Oil']
    assert result['instructions'] == 'Mix all ingredients.'


def test_get_nonexistent_recipe():
    recipe = Recipe()
    with pytest.raises(Exception):
        recipe.get_recipe('Pizza')


def test_file_persistence():
    recipe = Recipe()
    result_before = recipe.get_recipe('Pasta')
    assert result_before['ingredients'] == ['Tomato Sauce', 'Pasta', 'Cheese']
    assert result_before['instructions'] == 'Boil pasta and mix with sauce.'