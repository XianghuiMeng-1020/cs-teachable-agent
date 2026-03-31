import pytest
import os
from solution import organize_recipes

def setup_module(module):
    with open('recipes.txt', 'w') as file:
        file.write(\
            """
Pasta\nTomato, Basil, Garlic, Pasta\nBoil pasta\nCook sauce\nMix together\n\nCake\nFlour, Sugar, Eggs, Butter\nMix dry ingredients\nAdd eggs and butter\nBake\n\nSalad\nLettuce, Tomato, Cucumber\nChop all ingredients\nMix in a bowl\nServe\n""".strip())

def teardown_module(module):
    try:
        os.remove('recipes.txt')
    except FileNotFoundError:
        pass

def test_organize_recipes():
    result = organize_recipes('recipes.txt')
    expected = [
        {'title': 'Cake', 'ingredients': ['Flour', 'Sugar', 'Eggs', 'Butter'], 'instructions': ['Mix dry ingredients', 'Add eggs and butter', 'Bake']},
        {'title': 'Pasta', 'ingredients': ['Tomato', 'Basil', 'Garlic', 'Pasta'], 'instructions': ['Boil pasta', 'Cook sauce', 'Mix together']},
        {'title': 'Salad', 'ingredients': ['Lettuce', 'Tomato', 'Cucumber'], 'instructions': ['Chop all ingredients', 'Mix in a bowl', 'Serve']}
    ]
    assert result == expected

def test_organize_single_recipe():
    with open('single_recipe.txt', 'w') as file:
        file.write("Omelette\nEggs, Cheese\nBeat eggs\nCook on pan")
    result = organize_recipes('single_recipe.txt')
    expected = [
        {'title': 'Omelette', 'ingredients': ['Eggs', 'Cheese'], 'instructions': ['Beat eggs', 'Cook on pan']}
    ]
    os.remove('single_recipe.txt')
    assert result == expected

def test_organize_empty_file():
    open('empty.txt', 'w').close()
    result = organize_recipes('empty.txt')
    expected = []
    os.remove('empty.txt')
    assert result == expected

def test_with_no_instructions():
    with open('no_instructions.txt', 'w') as file:
        file.write("Smoothie\nBananas, Milk\n\n")
    result = organize_recipes('no_instructions.txt')
    expected = [
        {'title': 'Smoothie', 'ingredients': ['Bananas', 'Milk'], 'instructions': []}
    ]
    os.remove('no_instructions.txt')
    assert result == expected

def test_with_no_ingredients():
    with open('no_ingredients.txt', 'w') as file:
        file.write("Broth\n\nSimmer the broth\nSeason to taste")
    result = organize_recipes('no_ingredients.txt')
    expected = [
        {'title': 'Broth', 'ingredients': [], 'instructions': ['Simmer the broth', 'Season to taste']}
    ]
    os.remove('no_ingredients.txt')
    assert result == expected