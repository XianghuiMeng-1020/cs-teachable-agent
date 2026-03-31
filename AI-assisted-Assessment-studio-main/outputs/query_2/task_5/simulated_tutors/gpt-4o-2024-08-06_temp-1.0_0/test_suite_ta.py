from program import *
import os
import pytest
from program import sort_ingredients

def setup_module(module):
    with open('test_recipes.txt', 'w') as f:
        f.write('flour, sugar, baking soda\n')
        f.write('salt, pepper, garlic powder\n')
        f.write('sugar, cocoa powder, butter, milk\n')
        f.write('honey\n')
        f.write('zucchini, carrot, apple\n')

def teardown_module(module):
    os.remove('test_recipes.txt')
    if os.path.exists('test_sorted_recipes.txt'):
        os.remove('test_sorted_recipes.txt')

@pytest.mark.parametrize("test_input, expected_output", [
    ('test_recipes.txt', 'test_sorted_recipes.txt'),
])
def test_sort_ingredients(test_input, expected_output):
    sort_ingredients(test_input, expected_output)
    with open(expected_output, 'r') as f:
        lines = f.readlines()
    assert lines[0].strip() == 'baking soda, flour, sugar'
    assert lines[1].strip() == 'garlic powder, pepper, salt'
    assert lines[2].strip() == 'butter, cocoa powder, milk, sugar'
    assert lines[3].strip() == 'honey'
    assert lines[4].strip() == 'apple, carrot, zucchini'