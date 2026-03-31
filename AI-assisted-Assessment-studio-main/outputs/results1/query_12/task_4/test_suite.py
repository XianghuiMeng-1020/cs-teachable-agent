import pytest
import os
from solution_program import sort_recipes

def setup_module(module):
    with open('recipes.txt', 'w') as f:
        f.write('Pasta\nTomato\n2\nGarlic\n1\n\n')
        f.write('Soup\nWater\n1\nCarrot\n3\nTomato\n2\n\n')
        f.write('Salad\nLettuce\n1\nTomato\n1\nCucumber\n2\n')

def teardown_module(module):
    os.remove('recipes.txt')
    if os.path.exists('sorted_recipes.txt'):
        os.remove('sorted_recipes.txt')


def test_basic_sorting():
    sort_recipes('recipes.txt', 'sorted_recipes.txt')
    with open('sorted_recipes.txt', 'r') as f:
        content = f.read()
    expected_content = ('Pasta\nTomato\n2\nGarlic\n1\n\n'
                        'Salad\nLettuce\n1\nTomato\n1\nCucumber\n2\n\n'
                        'Soup\nWater\n1\nCarrot\n3\nTomato\n2\n')
    assert content == expected_content


def test_no_input_file():
    if os.path.exists('non_existing_file.txt'):
        os.remove('non_existing_file.txt')
    with pytest.raises(FileNotFoundError):
        sort_recipes('non_existing_file.txt', 'sorted_recipes.txt')


def test_empty_file():
    with open('empty_recipes.txt', 'w') as f:
        f.write('')
    sort_recipes('empty_recipes.txt', 'sorted_recipes.txt')
    with open('sorted_recipes.txt', 'r') as f:
        content = f.read()
    assert content == ''
    os.remove('empty_recipes.txt')


def test_single_recipe():
    with open('single_recipe.txt', 'w') as f:
        f.write('Bread\nFlour\n2\nWater\n1\n')
    sort_recipes('single_recipe.txt', 'sorted_recipes.txt')
    with open('sorted_recipes.txt', 'r') as f:
        content = f.read()
    assert content == 'Bread\nFlour\n2\nWater\n1\n'
    os.remove('single_recipe.txt')


def test_multiple_recipes_same_name():
    with open('same_name_recipes.txt', 'w') as f:
        f.write('Pie\nApple\n3\nFlour\n1\n\nPie\nPeach\n4\nSugar\n2\n')
    sort_recipes('same_name_recipes.txt', 'sorted_recipes.txt')
    with open('sorted_recipes.txt', 'r') as f:
        content = f.read()
    assert content == ('Pie\nApple\n3\nFlour\n1\n\n'
                       'Pie\nPeach\n4\nSugar\n2\n')
    os.remove('same_name_recipes.txt')