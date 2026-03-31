from solution_program import *
import pytest
import os
from solution_program import filter_ingredients

def setup_module(module):
    with open('test_recipes.txt', 'w') as f:
        f.write('Pasta Carbonara\nSpaghetti\nEggs\nParmesan Cheese\nPancetta\n\n')
        f.write('Chocolate Cake\nFlour\nCocoa Powder\nEggs\nMilk\nSugar\nButter\nBaking Powder\n\n')
        f.write('Fruit Salad\nApple\nBanana\nOrange\n')

def teardown_module(module):
    os.remove('test_recipes.txt')
    if os.path.exists('result_recipes.txt'):
        os.remove('result_recipes.txt')

class TestFilterIngredients:

    def test_filter_ingredients_exceeding(self):
        filter_ingredients('test_recipes.txt', 'result_recipes.txt', 4)
        with open('result_recipes.txt', 'r') as f:
            content = f.read()
            assert content == 'Pasta Carbonara\nSpaghetti\nEggs\nParmesan Cheese\nPancetta\n\n'

    def test_filter_ingredients_no_exceed(self):
        filter_ingredients('test_recipes.txt', 'result_recipes.txt', 8)
        with open('result_recipes.txt', 'r') as f:
            content = f.read()
            assert content == ('Pasta Carbonara\nSpaghetti\nEggs\nParmesan Cheese\nPancetta\n\n'
                               'Chocolate Cake\nFlour\nCocoa Powder\nEggs\nMilk\nSugar\nButter\nBaking Powder\n\n'
                               'Fruit Salad\nApple\nBanana\nOrange\n')

    def test_filter_no_recipes(self):
        filter_ingredients('test_recipes.txt', 'result_recipes.txt', 2)
        with open('result_recipes.txt', 'r') as f:
            content = f.read()
            assert content == ''

    def test_filter_all_recipes_removed(self):
        filter_ingredients('test_recipes.txt', 'result_recipes.txt', 0)
        with open('result_recipes.txt', 'r') as f:
            content = f.read()
            assert content == ''

    def test_filter_various_lines(self):
        filter_ingredients('test_recipes.txt', 'result_recipes.txt', 3)
        with open('result_recipes.txt', 'r') as f:
            content = f.read()
            assert content == ('Fruit Salad\nApple\nBanana\nOrange\n')