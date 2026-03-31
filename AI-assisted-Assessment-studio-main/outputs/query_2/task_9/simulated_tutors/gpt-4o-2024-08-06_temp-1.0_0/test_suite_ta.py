from program import *
import pytest
import os
from program import recipe_ingredients_calculator

def setup_module(module):
    with open('recipes.txt', 'w') as f:
        f.write('Pasta:tomato,basil,garlic,olive oil\n')
        f.write('French Toast:egg,milk,butter,sugar\n')
        f.write('Salad:lettuce,tomato,cucumber,olive oil\n')

def teardown_module(module):
    os.remove('recipes.txt')

def test_ingredients_sorted_uniq_1():
    assert recipe_ingredients_calculator('recipes.txt') == [
        'basil', 'butter', 'cucumber', 'egg', 'garlic', 'lettuce', 'milk', 'olive oil', 'sugar', 'tomato']


def test_ingredients_sorted_uniq_2():
    with open('recipes.txt', 'w') as f:
        f.write('Omelette:egg,milk,cheese,salt\n')
        f.write('Borscht:beetroot,carrot,potato,onion\n')
        f.write('Salsa:tomato,onion,jalapeno,cilantro\n')    
    assert recipe_ingredients_calculator('recipes.txt') == [
        'beetroot', 'carrot', 'cheese', 'cilantro', 'egg', 'jalapeno', 'milk', 'onion', 'potato', 'salt', 'tomato']


def test_no_recipes():
    with open('recipes.txt', 'w') as f:
        f.write('')
    assert recipe_ingredients_calculator('recipes.txt') == []


def test_single_recipe():
    with open('recipes.txt', 'w') as f:
        f.write('Sandwich:bread,butter,lettuce,tomato\n')
    assert recipe_ingredients_calculator('recipes.txt') == [
        'bread', 'butter', 'lettuce', 'tomato']


def test_duplicate_ingredients():
    with open('recipes.txt', 'w') as f:
        f.write('Dish:ingredient,ingredient,ingredient\nDishTwo:ingredient,ingredient\n')
    assert recipe_ingredients_calculator('recipes.txt') == ['ingredient']