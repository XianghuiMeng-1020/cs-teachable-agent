from program import *
import pytest
import os
from program import RecipeBook

defile_path = 'test_recipes.txt'

def setup_module(module):
    with open(file_path, 'w') as f:
        f.write('Pasta:tomato,cheese,basil\n')

def teardown_module(module):
    os.remove(file_path)

def test_load_recipes():
    rb = RecipeBook()
    rb.load_recipes(file_path)
    assert 'Pasta' in rb.recipes
    assert rb.recipes['Pasta'] == ['tomato', 'cheese', 'basil']

def test_add_recipe():
    rb = RecipeBook()
    rb.load_recipes(file_path)
    rb.add_recipe('Salad', ['lettuce', 'tomato', 'cucumber'], file_path)
    assert 'Salad' in rb.recipes
    assert rb.recipes['Salad'] == ['lettuce', 'tomato', 'cucumber']
    with open(file_path, 'r') as f:
        content = f.read()
    assert 'Salad:lettuce,tomato,cucumber' in content

def test_find_recipe_existing():
    rb = RecipeBook()
    rb.load_recipes(file_path)
    ingredients = rb.find_recipe('Pasta')
    assert ingredients == ['tomato', 'cheese', 'basil']

def test_find_recipe_nonexistent():
    rb = RecipeBook()
    with pytest.raises(ValueError) as excinfo:
        rb.find_recipe('Soup')
    assert str(excinfo.value) == 'Recipe not found'

def test_file_not_found():
    rb = RecipeBook()
    with pytest.raises(OSError):
        rb.load_recipes('nonexistent_file.txt')