from program import *
import pytest
import os
from program import RecipeManager

def setup_module(module):
    with open('recipes.txt', 'w') as f:
        f.write("Scrambled Eggs\neggs\nbutter\nmilk\n\nPancakes\nflour\neggs\nmilk\n")

def teardown_module(module):
    os.remove('recipes.txt')

def test_add_recipe():
    manager = RecipeManager()
    manager.add_recipe('Omelette', ['eggs', 'cheese', 'salt'])
    assert manager.get_recipe('Omelette') == ['eggs', 'cheese', 'salt']

def test_get_recipe_existing():
    manager = RecipeManager()
    assert manager.get_recipe('Scrambled Eggs') == ['eggs', 'butter', 'milk']

def test_get_recipe_non_existent():
    manager = RecipeManager()
    assert manager.get_recipe('Pizza') is None

def test_delete_recipe_existing():
    manager = RecipeManager()
    assert manager.delete_recipe('Pancakes') is True
    assert manager.get_recipe('Pancakes') is None

def test_delete_recipe_non_existent():
    manager = RecipeManager()
    assert manager.delete_recipe('Burger') is False