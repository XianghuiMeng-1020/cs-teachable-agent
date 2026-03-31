from program import *
import pytest

from program import calculate_spices

def test_spices_basic_case():
    dishes = ['Salad', 'Soup', 'Curry', 'Grill', 'Salad']
    assert calculate_spices(dishes) == [4, 3, 5, 7]


def test_multiple_dishes_of_same_type():
    dishes = ['Salad', 'Salad', 'Salad']
    assert calculate_spices(dishes) == [6, 0, 0, 0]


def test_no_dishes():
    dishes = []
    assert calculate_spices(dishes) == [0, 0, 0, 0]


def test_different_dishes():
    dishes = ['Soup', 'Soup', 'Curry']
    assert calculate_spices(dishes) == [0, 6, 5, 0]


def test_maximum_different_dishes():
    dishes = ['Salad', 'Soup', 'Curry', 'Grill'] * 25
    assert calculate_spices(dishes) == [50, 75, 125, 175]
