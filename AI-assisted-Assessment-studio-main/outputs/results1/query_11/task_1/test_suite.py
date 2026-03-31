import pytest
from solution_program import check_ingredient_availability

def test_available_case():
    ingredients = ['Flour 1000', 'Sugar 500', 'Eggs 24']
    required_item = 'Sugar'
    required_quantity = 400
    result = check_ingredient_availability(ingredients, required_item, required_quantity)
    assert result == 'Available'

def test_not_enough_quantity():
    ingredients = ['Flour 1000', 'Sugar 500', 'Eggs 24']
    required_item = 'Sugar'
    required_quantity = 600
    result = check_ingredient_availability(ingredients, required_item, required_quantity)
    assert result == 'Not Available'

def test_item_not_in_list():
    ingredients = ['Flour 1000', 'Sugar 500', 'Eggs 24']
    required_item = 'Milk'
    required_quantity = 2
    result = check_ingredient_availability(ingredients, required_item, required_quantity)
    assert result == 'Not Available'

def test_exact_quantity():
    ingredients = ['Flour 1000', 'Sugar 500', 'Eggs 24']
    required_item = 'Eggs'
    required_quantity = 24
    result = check_ingredient_availability(ingredients, required_item, required_quantity)
    assert result == 'Available'

def test_zero_quantity_needed():
    ingredients = ['Flour 1000', 'Sugar 500', 'Eggs 24']
    required_item = 'Flour'
    required_quantity = 0
    result = check_ingredient_availability(ingredients, required_item, required_quantity)
    assert result == 'Available'
