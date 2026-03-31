from solution_program import *
import os
import pytest
from solution_program import categorize_recipes

def setup_module(module):
    os.makedirs('test_recipes', exist_ok=True)
    with open('test_recipes/recipe1.txt', 'w') as f:
        f.write("apple\nbanana\nmilk\n")
    with open('test_recipes/recipe2.txt', 'w') as f:
        f.write("sugar\nsalt\nflour\neggs\nbutter\n")
    with open('test_recipes/recipe3.txt', 'w') as f:
        f.write("rice\nchicken\nsalt\npepper\ntomatoes\ncucumbers\nlettuce\n")
    with open('test_recipes/recipe4.txt', 'w') as f:
        f.write("lemon\nginger\ncoriander\npepper\nturmeric\ngarlic\nonion\nyogurt\nsalt\n")
    with open('test_recipes/recipe5.txt', 'w') as f:
        f.write("potato\n")

def teardown_module(module):
    for filename in os.listdir('test_recipes'):
        file_path = os.path.join('test_recipes', filename)
        os.remove(file_path)
    os.rmdir('test_recipes')
    if os.path.exists('output.txt'):
        os.remove('output.txt')

@pytest.mark.parametrize("expected_lines", [
    "recipe1.txt: simple",
    "recipe2.txt: simple",
    "recipe3.txt: simple",
    "recipe4.txt: complex",
    "recipe5.txt: simple",
])
def test_categorize_recipes(expected_lines):
    categorize_recipes('test_recipes', 'output.txt')
    with open('output.txt') as f:
        lines = f.read().strip().split('\n')
    assert expected_lines in lines