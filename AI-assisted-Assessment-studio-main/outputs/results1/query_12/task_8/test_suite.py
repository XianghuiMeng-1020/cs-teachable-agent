import pytest
import os
from solution import can_cook_recipe

files_content = {
    'ingredients.txt': """
    flour,500
    sugar,200
    eggs,12
    butter,100
    salt,50
    """.strip()
}


def setup_module(module):
    with open('ingredients.txt', 'w') as f:
        f.write(files_content['ingredients.txt'])


def teardown_module(module):
    os.remove('ingredients.txt')


def test_can_cook_exact_amount():
    recipe = {'flour': 500, 'sugar': 200}
    assert can_cook_recipe(recipe, 'ingredients.txt') is True


def test_can_cook_less_than_available():
    recipe = {'flour': 300, 'sugar': 100}
    assert can_cook_recipe(recipe, 'ingredients.txt') is True


def test_cannot_cook_not_enough_flour():
    recipe = {'flour': 600, 'sugar': 200}
    assert can_cook_recipe(recipe, 'ingredients.txt') is False


def test_cannot_cook_not_enough_sugar():
    recipe = {'flour': 400, 'sugar': 250}
    assert can_cook_recipe(recipe, 'ingredients.txt') is False


def test_cannot_cook_missing_ingredient():
    recipe = {'flour': 500, 'chocolate': 50}
    assert can_cook_recipe(recipe, 'ingredients.txt') is False