import os
import pytest
from solution import Recipe

def setup_module(module):
    with open('test_recipe1.txt', 'w') as f:
        f.write("Scrambled Eggs\nEggs, Salt, Pepper\nBeat the eggs and cook them.")
    with open('test_recipe2.txt', 'w') as f:
        f.write("Pasta\nPasta, Tomato Sauce\nBoil pasta and add sauce.")
    with open('test_recipe3.txt', 'w') as f:
        f.write("Pancakes\nFlour, Milk, Eggs\nMix ingredients and fry.")

def teardown_module(module):
    os.remove('test_recipe1.txt')
    os.remove('test_recipe2.txt')
    os.remove('test_recipe3.txt')
    if os.path.exists('output_recipe.txt'):
        os.remove('output_recipe.txt')


def test_load_recipe_valid_file():
    recipe = Recipe.load_from_file('test_recipe1.txt')
    assert recipe.name == "Scrambled Eggs"
    assert recipe.ingredients == ["Eggs", "Salt", "Pepper"]
    assert recipe.instructions == "Beat the eggs and cook them."


def test_load_recipe_another_valid_file():
    recipe = Recipe.load_from_file('test_recipe2.txt')
    assert recipe.name == "Pasta"
    assert recipe.ingredients == ["Pasta", "Tomato Sauce"]
    assert recipe.instructions == "Boil pasta and add sauce."


def test_load_recipe_file_not_found():
    recipe = Recipe.load_from_file('non_existent_file.txt')
    assert recipe is None


def test_save_and_load_recipe():
    scrambled_eggs = Recipe("Scrambled Eggs", ["Eggs", "Salt", "Pepper"], "Beat the eggs and cook them.")
    scrambled_eggs.save_to_file('output_recipe.txt')
    loaded_recipe = Recipe.load_from_file('output_recipe.txt')
    assert loaded_recipe.name == scrambled_eggs.name
    assert loaded_recipe.ingredients == scrambled_eggs.ingredients
    assert loaded_recipe.instructions == scrambled_eggs.instructions


def test_load_recipe_malformed_file():
    with open('malformed_recipe.txt', 'w') as f:
        f.write("Invalid Content")  # Not enough lines
    recipe = Recipe.load_from_file('malformed_recipe.txt')
    assert recipe is None
    os.remove('malformed_recipe.txt')