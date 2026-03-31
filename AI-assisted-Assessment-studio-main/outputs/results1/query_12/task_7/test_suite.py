import pytest
import os
from solution import summarize_recipes

def setup_module(module):
    with open('recipes.txt', 'w') as f:
        f.write("Pasta with stove\nCake with oven\nSalad with no_cook\nRoast with oven, stove\nSoup on the stove\n")

    with open('empty_recipes.txt', 'w') as f:
        f.write("")

    with open('no_keywords.txt', 'w') as f:
        f.write("Fruit salad\nIce cream\nWatermelon\n")

    with open('complex_recipes.txt', 'w') as f:
        f.write("Multi-cooker, slow-cooker\nOven roasted chicken\nStove-top popcorn\nNo_cook juice\n")


def teardown_module(module):
    os.remove('recipes.txt')
    os.remove('empty_recipes.txt')
    os.remove('no_keywords.txt')
    os.remove('complex_recipes.txt')


def test_summarize_recipes_basic():
    result = summarize_recipes('recipes.txt')
    assert result == {'stove': 3, 'oven': 2, 'no_cook': 1}


def test_summarize_recipes_empty():
    result = summarize_recipes('empty_recipes.txt')
    assert result == {'stove': 0, 'oven': 0, 'no_cook': 0}


def test_summarize_recipes_no_keywords():
    result = summarize_recipes('no_keywords.txt')
    assert result == {'stove': 0, 'oven': 0, 'no_cook': 0}


def test_summarize_recipes_complex():
    result = summarize_recipes('complex_recipes.txt')
    assert result == {'stove': 1, 'oven': 1, 'no_cook': 1}


def test_summarize_recipes_mixed_case():
    with open('mixed_case_recipes.txt', 'w') as f:
        f.write("Cooking on Stove\nBaking in Oven\nFresh no_cook salad\n")
    result = summarize_recipes('mixed_case_recipes.txt')
    assert result == {'stove': 1, 'oven': 1, 'no_cook': 1}
    os.remove('mixed_case_recipes.txt')