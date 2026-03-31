from program import *
import pytest
import os
from program import format_recipe

def setup_module(module):
    with open('test_recipes.txt', 'w') as f:
        f.write(
            "Chocolate Cake--flour, sugar, cocoa, baking powder--mix ingredients, bake for 30m\n"
            "Pasta--pasta, tomatoes, garlic--boil pasta, sauté tomatoes and garlic\n"
            "Sandwich--bread, cheese, ham--assemble, grill\n"
"
        )

def teardown_module(module):
    os.remove('test_recipes.txt')
    os.remove('formatted_recipes.txt')


def test_format_recipe_1():
    format_recipe('test_recipes.txt', 'formatted_recipes.txt')
    with open('formatted_recipes.txt', 'r') as f:
        content = f.read()
    assert content.count("Recipe Title") == 3

def test_format_recipe_2():
    format_recipe('test_recipes.txt', 'formatted_recipes.txt')
    with open('formatted_recipes.txt', 'r') as f:
        content = f.read()
    assert "Ingredients:\n- flour\n- sugar\n- cocoa\n- baking powder" in content


def test_format_recipe_3():
    format_recipe('test_recipes.txt', 'formatted_recipes.txt')
    with open('formatted_recipes.txt', 'r') as f:
        content = f.read()
    assert "Method:\nboil pasta, sauté tomatoes and garlic" in content

def test_format_recipe_4():
    with open('formatted_recipes.txt', 'r') as f:
        content = f.read()
    assert content.startswith("Recipe Title: Chocolate Cake")

def test_format_recipe_5():
    with open('formatted_recipes.txt', 'r') as f:
        content = f.read()
    assert content.endswith("grill\n\n")