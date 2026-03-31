def get_recipes_by_category(filename, category_name):
    recipes = []
    
    # Attempt to open and read the file
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Strip and split the line to get its components
                parts = line.strip().split(';')
                if len(parts) != 4:
                    # Skip lines not having exactly 4 parts
                    continue
                name, ingredients, prep_time, category = parts
                if category.strip().lower() == category_name.lower():
                    recipes.append(name.strip())
    except FileNotFoundError:
        return []
    
    return recipes

import pytest
import os
from solution import get_recipes_by_category

data = '''Pasta;Tomato,Garlic,Olive Oil;15 minutes;Main Course
Apple Pie;Apple,Flour,Sugar;90 minutes;Dessert
Bruschetta;Tomato,Basil,Olive Oil;10 minutes;Appetizer
Chocolate Cake;Cocoa,Butter,Flour,Milk;120 minutes;Dessert
Salad;Lettuce,Tomato,Cucumber;5 minutes;Appetizer
'''  

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