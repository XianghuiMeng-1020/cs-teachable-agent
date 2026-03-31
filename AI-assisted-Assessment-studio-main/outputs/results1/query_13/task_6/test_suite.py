import pytest
import os
from inventory import process_ingredient_usage


def setup_module(module):
    with open('test_file.txt', 'w') as f:
        f.write("Flour:500\nSugar:200\nEggs:70\nButter:200\nFlour:200\n")
    with open('test_file_bad.txt', 'w') as f:
        f.write("Flour:300\nSugar:a50\nEggs:30\nMilk:invalid\nEggs:-20\nFlour:100\n\n")


def teardown_module(module):
    os.remove('test_file.txt')
    os.remove('test_file_bad.txt')


def test_process_ingredient_usage():
    result = process_ingredient_usage('test_file.txt')
    assert result == {"Flour": 700, "Sugar": 200, "Eggs": 70, "Butter": 200}


def test_process_ingredient_usage_with_errors():
    result = process_ingredient_usage('test_file_bad.txt')
    assert result == {"Flour": 400, "Eggs": 10}


def test_empty_file():
    with open('empty_file.txt', 'w') as f:
        f.write("")
    result = process_ingredient_usage('empty_file.txt')
    assert result == {}
    os.remove('empty_file.txt')


def test_incorrect_format_handling():
    with open('incorrect_format.txt', 'w') as f:
        f.write("Flour:\nSugar:500\nEggs:70\nButter:200\n")
    result = process_ingredient_usage('incorrect_format.txt')
    assert result == {"Sugar": 500, "Eggs": 70, "Butter": 200}
    os.remove('incorrect_format.txt')


def test_file_with_missing_colon():
    with open('missing_colon.txt', 'w') as f:
        f.write("Flour500\nSugar:100\nMilk200\nEggs:50\n")
    result = process_ingredient_usage('missing_colon.txt')
    assert result == {"Sugar": 100, "Eggs": 50}
    os.remove('missing_colon.txt')
