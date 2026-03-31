from program import *
import pytest
import os

def setup_module(module):
    os.makedirs('recipes', exist_ok=True)
    with open('recipes/recipe1.txt', 'w') as f:
        f.write("Chop vegetables - 10 minutes\nBoil water - 5 minutes\nCook pasta - 15 minutes\n")
    with open('recipes/recipe2.txt', 'w') as f:
        f.write("Mix ingredients - 5 minutes\nBake - 20 minutes\nCool - 10 minutes\n")
    with open('recipes/recipe3.txt', 'w') as f:
        f.write("Prepare sauce - 10 minutes\nGrill chicken - 25 minutes\n")
    with open('recipes/recipe4.txt', 'w') as f:
        f.write("Steam rice - 15 minutes\nFry vegetables - 10 minutes\n")
    with open('recipes/recipe5.txt', 'w') as f:
        f.write("Season soup - 5 minutes\nSimmer - 30 minutes\n")

def teardown_module(module):
    try:
        os.remove('cooking_times.txt')
        os.remove('recipes/recipe1.txt')
        os.remove('recipes/recipe2.txt')
        os.remove('recipes/recipe3.txt')
        os.remove('recipes/recipe4.txt')
        os.remove('recipes/recipe5.txt')
        os.rmdir('recipes')
    except FileNotFoundError:
        pass

from program import estimate_cooking_times

def test_estimate_cooking_times():
    estimate_cooking_times()
    with open('cooking_times.txt', 'r') as f:
        lines = f.readlines()
    assert lines[0].strip() == 'Recipe 1: 30 minutes'
    assert lines[1].strip() == 'Recipe 2: 35 minutes'
    assert lines[2].strip() == 'Recipe 3: 35 minutes'
    assert lines[3].strip() == 'Recipe 4: 25 minutes'
    assert lines[4].strip() == 'Recipe 5: 35 minutes'

def test_no_recipes_directory():
    os.rmdir('recipes')
    estimate_cooking_times()
    assert os.path.isfile('cooking_times.txt') == False
    os.makedirs('recipes', exist_ok=True)

def test_empty_recipe_file():
    with open('recipes/recipe6.txt', 'w') as f:
        pass
    estimate_cooking_times()
    with open('cooking_times.txt', 'r') as f:
        lines = f.readlines()
    assert lines[5].strip() == 'Recipe 6: 0 minutes'

    os.remove('recipes/recipe6.txt')

def test_inconsistent_file_names():
    with open('recipes/my_special_recipe.txt', 'w') as f:
        f.write("Grill fish - 20 minutes\n")
    try:
        estimate_cooking_times()
        with open('cooking_times.txt', 'r') as f:
            lines = f.readlines()
        len_recipes = len([l for l in lines if l.startswith('Recipe')])
        assert len_recipes == 5  # The count should remain 5 as non-sequential names should be ignored
    finally:
        os.remove('recipes/my_special_recipe.txt')

def test_multiple_sessions():
    estimate_cooking_times()
    estimate_cooking_times()
    with open('cooking_times.txt', 'r') as f:
        lines = f.readlines()
    assert len(lines) == 5  # Verify no duplication