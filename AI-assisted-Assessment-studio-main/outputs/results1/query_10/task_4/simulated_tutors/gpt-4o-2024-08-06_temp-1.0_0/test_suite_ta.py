from program import *
import pytest
import os
from program import RecipeManager


def setup_module(module):
    with open('recipes.txt', 'w') as f:
        f.write("Pancakes\n" "Omelette\n" "Salad\n")

def teardown_module(module):
    if os.path.exists('recipes.txt'):
        os.remove('recipes.txt')


def test_initialization_from_file():
    manager = RecipeManager()
    assert sorted(manager.list_recipes()) == ['Omelette', 'Pancakes', 'Salad']


def test_add_recipe_successful():
    manager = RecipeManager()
    manager.add_recipe('Soup')
    assert sorted(manager.list_recipes()) == ['Omelette', 'Pancakes', 'Salad', 'Soup']


def test_add_duplicate_recipe():
    manager = RecipeManager()
    manager.add_recipe('Pancakes')
    assert sorted(manager.list_recipes()) == ['Omelette', 'Pancakes', 'Salad']


def test_remove_existing_recipe():
    manager = RecipeManager()
    manager.remove_recipe('Salad')
    assert sorted(manager.list_recipes()) == ['Omelette', 'Pancakes']


def test_remove_non_existent_recipe():
    manager = RecipeManager()
    manager.remove_recipe('Pizza')
    assert sorted(manager.list_recipes()) == ['Omelette', 'Pancakes', 'Salad']


def test_recipe_persistence():
    manager = RecipeManager()
    manager.add_recipe('Pie')
    manager.remove_recipe('Omelette')
    manager2 = RecipeManager()  # Re-initialize to see if changes persist
    assert sorted(manager2.list_recipes()) == ['Pancakes', 'Pie', 'Salad']