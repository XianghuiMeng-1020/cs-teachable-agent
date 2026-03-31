from solution_program import *
import pytest
from solution_program import calculate_ingredient_amounts

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    # Setup code if needed
    yield
    # Teardown code if needed

def test_single_ingredient_single_serving():
    ingredient_list = ["Sugar:100g"]
    desired_servings = 3
    expected = ["Sugar:300g"]
    assert calculate_ingredient_amounts(ingredient_list, desired_servings) == expected


def test_multiple_ingredients_multiple_servings():
    ingredient_list = ["Butter:50g", "Milk:200ml", "Eggs:2pcs"]
    desired_servings = 4
    expected = ["Butter:200g", "Milk:800ml", "Eggs:8pcs"]
    assert calculate_ingredient_amounts(ingredient_list, desired_servings) == expected


def test_no_servings():
    ingredient_list = ["Flour:50g"]
    desired_servings = 0
    expected = ["Flour:0g"]
    assert calculate_ingredient_amounts(ingredient_list, desired_servings) == expected


def test_large_numbers():
    ingredient_list = ["Rice:1000g"]
    desired_servings = 100
    expected = ["Rice:100000g"]
    assert calculate_ingredient_amounts(ingredient_list, desired_servings) == expected


def test_single_ingredient_edge_case():
    ingredient_list = ["Yeast:1g"]
    desired_servings = 1
    expected = ["Yeast:1g"]
    assert calculate_ingredient_amounts(ingredient_list, desired_servings) == expected
