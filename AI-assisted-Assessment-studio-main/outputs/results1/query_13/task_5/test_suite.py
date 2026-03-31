import pytest
import os
from solution import calculate_average_cooking_time

def setup_module(module):
    with open('test_cooking_times.txt', 'w') as f:
        f.write("Spaghetti,20\n")
        f.write("Pizza,25\n")
        f.write("\n")
        f.write("Ice Cream\n")
        f.write("Burger,15\n")
    with open('empty_file.txt', 'w') as f:
        pass
    with open('invalid_lines.txt', 'w') as f:
        f.write("Salt,\n")
        f.write("Pepper,,10\n")


def teardown_module(module):
    os.remove('test_cooking_times.txt')
    os.remove('empty_file.txt')
    os.remove('invalid_lines.txt')


def test_average_cooking_time():
    assert calculate_average_cooking_time('test_cooking_times.txt') == 20.0

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        calculate_average_cooking_time('non_existent_file.txt')


def test_empty_file():
    with pytest.raises(ValueError, match="No valid cooking times found"):
        calculate_average_cooking_time('empty_file.txt')


def test_file_with_invalid_lines():
    with open('mixed_lines.txt', 'w') as f:
        f.write("Salt,\n")
        f.write("Spaghetti,30\n")
        f.write("Pepper,,10\n")
        f.write("Soup,10\n")
    try:
        assert calculate_average_cooking_time('mixed_lines.txt') == 20.0
    finally:
        os.remove('mixed_lines.txt')


def test_all_invalid_lines():
    with pytest.raises(ValueError, match="No valid cooking times found"):
        calculate_average_cooking_time('invalid_lines.txt')