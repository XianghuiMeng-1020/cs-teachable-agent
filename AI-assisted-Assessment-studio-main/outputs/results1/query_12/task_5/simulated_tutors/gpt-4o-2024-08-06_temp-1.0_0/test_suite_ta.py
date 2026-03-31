from program import *
import pytest
import os
from program import generate_ingredient_report

# Test file setup
recipes_file = 'recipes.txt'
ingredient_report_file = 'ingredient_report.txt'

def setup_module(module):
    with open(recipes_file, 'w') as f:
        f.write("Pasta | salt, olive oil, garlic\n")
        f.write("Salad | lettuce, olive oil, salt\n")
        f.write("Soup | water, salt, carrots\n")
        f.write("Bread | flour, water, salt, yeast\n")
        f.write("Stew | beef, potatoes, carrots, salt\n")
        f.write("Invalid line without proper delimiter\n")
        f.write("Pizza | flour, water, yeast\n")


def teardown_module(module):
    try:
        os.remove(recipes_file)
        os.remove(ingredient_report_file)
    except OSError:
        pass


def test_generate_ingredient_report_general():
    generate_ingredient_report()
    with open(ingredient_report_file, 'r') as f:
        output = f.readlines()
    expected_output = [
        'salt: 5\n',
        'water: 3\n',
        'olive oil: 2\n',
        'carrots: 2\n',
        'flour: 2\n',
        'yeast: 2\n',
        'lettuce: 1\n',
        'beef: 1\n',
        'potatoes: 1\n',
        'garlic: 1\n'
    ]
    assert output == expected_output


def test_generate_ingredient_report_no_file():
    os.remove(recipes_file)
    generate_ingredient_report()
    assert os.path.exists(ingredient_report_file)
    with open(ingredient_report_file, 'r') as f:
        output = f.read()
    assert output == ""


def test_generate_ingredient_report_empty_file():
    with open(recipes_file, 'w') as f:
        pass
    generate_ingredient_report()
    with open(ingredient_report_file, 'r') as f:
        output = f.read()
    assert output == ""


def test_generate_ingredient_report_non_conforming_lines():
    with open(recipes_file, 'w') as f:
        f.write("Invalid line\n")
    generate_ingredient_report()
    with open(ingredient_report_file, 'r') as f:
        output = f.read()
    assert output == ""


def test_generate_ingredient_report_case_sensitivity():
    with open(recipes_file, 'w') as f:
        f.write("Pasta | Salt, olive oil, garlic\n")
        f.write("Salad | lettuce, OLIVE oil, salt\n")
    generate_ingredient_report()
    with open(ingredient_report_file, 'r') as f:
        output = f.readlines()
    expected_output = [
        'Salt: 1\n',
        'olive oil: 1\n',
        'garlic: 1\n',
        'lettuce: 1\n',
        'OLIVE oil: 1\n',
        'salt: 1\n'
    ]
    assert output == expected_output
