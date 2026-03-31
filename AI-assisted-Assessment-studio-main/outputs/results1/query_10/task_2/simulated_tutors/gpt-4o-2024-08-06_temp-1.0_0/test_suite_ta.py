from program import *
import pytest
import os
from program import Recipe, save_recipe_to_file, load_recipes_from_file

def setup_module(module):
    with open('test_recipes.txt', 'w') as f:
        f.write('Pasta:tomato,basil,garlic\n')
        f.write('Sandwich:bread,ham,cheese\n')

    # Create an empty file for tests
    with open('empty_recipes.txt', 'w') as f:
        pass

def teardown_module(module):
    os.remove('test_recipes.txt')
    os.remove('empty_recipes.txt')
    if os.path.exists('output_recipes.txt'):
        os.remove('output_recipes.txt')

def test_recipe_to_string():
    recipe = Recipe("Soup", ["carrot", "celery", "onion"])
    assert recipe.to_string() == "Soup:carrot,celery,onion"

def test_recipe_from_string():
    recipe_string = "Cake:flour,sugar,eggs"
    recipe = Recipe.from_string(recipe_string)
    assert recipe.name == "Cake"
    assert recipe.ingredients == ["flour", "sugar", "eggs"]

def test_save_recipe_to_file():
    recipe = Recipe("Salad", ["lettuce", "tomato", "cucumber"])
    save_recipe_to_file(recipe, 'output_recipes.txt')
    with open('output_recipes.txt', 'r') as f:
        assert f.read().strip() == "Salad:lettuce,tomato,cucumber"

def test_load_recipes_from_file():
    recipes = load_recipes_from_file('test_recipes.txt')
    assert len(recipes) == 2
    assert recipes[0].name == "Pasta"
    assert recipes[0].ingredients == ["tomato", "basil", "garlic"]
    assert recipes[1].name == "Sandwich"
    assert recipes[1].ingredients == ["bread", "ham", "cheese"]

def test_load_recipes_from_empty_file():
    recipes = load_recipes_from_file('empty_recipes.txt')
    assert recipes == []

def test_load_recipes_from_nonexistent_file():
    recipes = load_recipes_from_file('nonexistent_recipes.txt')
    assert recipes == []