from solution_program import *
import pytest
from solution_program import estimate_cooking_time


def test_estimate_cooking_time_valid_dishes():
    assert estimate_cooking_time(['Salad', 'Soup']) == 55


def test_estimate_cooking_time_single_dish():
    assert estimate_cooking_time(['Ratatouille']) == 55


def test_estimate_cooking_time_mixed_strings_and_non_strings():
    with pytest.raises(ValueError, match='Invalid item in dish list'):
        estimate_cooking_time(['Pasta', 123, 'Steak'])


def test_estimate_cooking_time_all_valid():
    assert estimate_cooking_time(['Cake', 'Pie', 'Pudding', 'Brownie']) == 115


def test_estimate_cooking_time_empty_list():
    assert estimate_cooking_time([]) == 0