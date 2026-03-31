from solution_program import *
import pytest
import os
from solution_program import Recipe

def setup_module(module):
    with open('test_recipe.txt', 'w') as f:
        f.write("""Recipe: Spaghetti
Ingredients:
- Pasta
- Tomato sauce
Cooking Method:
Boil pasta. Add sauce.
""")

def teardown_module(module):
    if os.path.exists('test_recipe.txt'):
        os.remove('test_recipe.txt')
    if os.path.exists('new_test_recipe.txt'):
        os.remove('new_test_recipe.txt')


def test_recipe_initialization():
    recipe = Recipe('Pancakes', ['Flour', 'Milk', 'Eggs'], 'Fry light batter.')
    assert recipe.name == 'Pancakes'
    assert recipe.ingredients == ['Flour', 'Milk', 'Eggs']
    assert recipe.cooking_method == 'Fry light batter.'


def test_add_ingredient():
    recipe = Recipe('Salad', ['Lettuce', 'Tomato'], 'Mix together.')
    recipe.add_ingredient('Cucumber')
    assert 'Cucumber' in recipe.ingredients


def test_remove_ingredient():
    recipe = Recipe('Smoothie', ['Banana', 'Milk'], 'Blend until smooth.')
    recipe.remove_ingredient('Milk')
    assert 'Milk' not in recipe.ingredients


def test_remove_non_existent_ingredient():
    recipe = Recipe('Omelette', ['Eggs', 'Salt'], 'Whisk eggs and fry.')
    with pytest.raises(ValueError, match="Ingredient not found"):
        recipe.remove_ingredient('Pepper')


def test_save_to_file():
    recipe = Recipe('Tea', ['Water', 'Tea leaves'], 'Boil water, steep leaves.')
    recipe.save_to_file('new_test_recipe.txt')
    with open('new_test_recipe.txt', 'r') as f:
        content = f.read()
    assert content == """Recipe: Tea
Ingredients:
- Water
- Tea leaves
Cooking Method:
Boil water, steep leaves.
"""


def test_load_from_file():
    recipe = Recipe('Default', [], '')
    recipe.load_from_file('test_recipe.txt')
    assert recipe.name == 'Spaghetti'
    assert recipe.ingredients == ['Pasta', 'Tomato sauce']
    assert recipe.cooking_method == 'Boil pasta. Add sauce.'


def test_load_from_non_existent_file():
    recipe = Recipe('Empty', [], '')
    try:
        recipe.load_from_file('non_existent.txt')
    except FileNotFoundError:
        assert recipe.name == 'Empty'
        assert recipe.ingredients == []
        assert recipe.cooking_method == ''