from solution_program import *
import pytest
import os
from solution_program import RecipeManager

def setup_module(module):
    with open('recipes.txt', 'w') as f:
        f.write("Pasta\nTomato Sauce, Pasta\nBoil pasta, add sauce.\n")


def teardown_module(module):
    try:
        os.remove('recipes.txt')
    except FileNotFoundError:
        pass


def test_add_recipe():
    manager = RecipeManager()
    manager.add_recipe('Salad', ['Lettuce', 'Tomatoes'], 'Mix all ingredients.')
    with open('recipes.txt', 'r') as f:
        content = f.read()
    assert 'Salad' in content
    assert 'Lettuce, Tomatoes' in content
    assert 'Mix all ingredients.' in content


def test_get_existing_recipe():
    manager = RecipeManager()
    recipe = manager.get_recipe('Pasta')
    assert recipe == "Pasta\nIngredients: Tomato Sauce, Pasta\nSteps: Boil pasta, add sauce."


def test_get_non_existing_recipe():
    manager = RecipeManager()
    recipe = manager.get_recipe('Pizza')
    assert recipe == "Recipe not found"


def test_file_not_exist_get_recipe():
    os.remove('recipes.txt')
    manager = RecipeManager()
    recipe = manager.get_recipe('Pasta')
    assert recipe == "Recipe not found"


def test_add_recipe_with_previous_exception():
    setup_module(None)  # Reset file to ensure controlled state
    manager = RecipeManager()
    os.remove('recipes.txt')
    manager.add_recipe('Sandwich', ['Bread', 'Ham'], 'Put ham between bread.')
    with open('recipes.txt', 'r') as f:
        content = f.read()
    assert 'Sandwich' in content
    assert 'Bread, Ham' in content
    assert 'Put ham between bread.' in content
