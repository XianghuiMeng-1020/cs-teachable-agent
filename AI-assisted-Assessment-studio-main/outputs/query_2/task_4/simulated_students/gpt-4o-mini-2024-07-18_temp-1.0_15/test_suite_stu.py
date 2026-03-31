from solution_program import *
import pytest
import os
from solution_program import organize_recipes

def setup_module(module):
    with open('recipes.txt', 'w') as f:
        f.write("""/****
NAME
Italian Pasta
---
INGREDIENTS
Pasta, Tomatoes, Olive Oil, Basil
****/

/****
NAME
Chocolate Cake
---
INGREDIENTS
Cocoa, Flour, Sugar, Eggs
****/

/****
NAME
Vegetable Soup
---
INGREDIENTS
Carrots, Onion, Tomatoes, Celery
****/

/****
NAME
Apple Pie
---
INGREDIENTS
Apples, Flour, Sugar, Cinnamon
****/
""")

def teardown_module(module):
    os.remove('recipes.txt')


def test_organize_recipes_single_case():
    assert organize_recipes('recipes.txt') == ['Apple Pie', 'Chocolate Cake', 'Italian Pasta', 'Vegetable Soup']


def test_empty_file():
    with open('empty.txt', 'w') as f:
        pass
    result = organize_recipes('empty.txt')
    assert result == []
    os.remove('empty.txt')


def test_no_recipes_block():
    with open('noblock.txt', 'w') as f:
        f.write("Some random text not in block comment")
    result = organize_recipes('noblock.txt')
    assert result == []
    os.remove('noblock.txt')


def test_incomplete_recipe():
    with open('incomplete.txt', 'w') as f:
        f.write("""/****
NAME
Broken Recipe

""")
    result = organize_recipes('incomplete.txt')
    assert result == []
    os.remove('incomplete.txt')


def test_unsorted_input():
    with open('unsorted.txt', 'w') as f:
        f.write("""/****
NAME
Zebra Cake
---
INGREDIENTS
Chocolate, Zebra print
****/

/****
NAME
Apple Tart
---
INGREDIENTS
Apples, Cinnamon
****/

/****
NAME
Banana Bread
---
INGREDIENTS
Bananas, Flour, Baking Soda
****/
""")
    result = organize_recipes('unsorted.txt')
    assert result == ['Apple Tart', 'Banana Bread', 'Zebra Cake']
    os.remove('unsorted.txt')
