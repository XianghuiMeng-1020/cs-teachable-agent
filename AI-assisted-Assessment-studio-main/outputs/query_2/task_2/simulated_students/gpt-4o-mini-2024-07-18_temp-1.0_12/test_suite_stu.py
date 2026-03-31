from solution_program import *
import pytest
import os
from solution_program import get_recipes_by_category

# Sample recipe file data
data = '''Pasta;Tomato,Garlic,Olive Oil;15 minutes;Main Course
Apple Pie;Apple,Flour,Sugar;90 minutes;Dessert
Bruschetta;Tomato,Basil,Olive Oil;10 minutes;Appetizer
Chocolate Cake;Cocoa,Butter,Flour,Milk;120 minutes;Dessert
Salad;Lettuce,Tomato,Cucumber;5 minutes;Appetizer
'''  # Note no trailing newline


def setup_module(module):
    with open('recipes.txt', 'w') as file:
        file.write(data)


def teardown_module(module):
    os.remove('recipes.txt')


def test_main_course_recipes():
    assert get_recipes_by_category('recipes.txt', 'Main Course') == ['Pasta']


def test_dessert_recipes():
    assert get_recipes_by_category('recipes.txt', 'Dessert') == ['Apple Pie', 'Chocolate Cake']


def test_appetizer_recipes():
    assert get_recipes_by_category('recipes.txt', 'Appetizer') == ['Bruschetta', 'Salad']


def test_no_matching_category():
    assert get_recipes_by_category('recipes.txt', 'Beverage') == []


def test_file_not_found():
    assert get_recipes_by_category('non_existing_file.txt', 'Appetizer') == []
