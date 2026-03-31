import pytest
from solution_program import calculate_total_cost

setup_module = lambda module: None
teardown_module = lambda module: None

def test_calculate_total_cost_basic():
    recipe_data = {
        "Pancake": [("Flour", 2), ("Egg", 3), ("Milk", 1)],
        "Omelette": [("Egg", 4), ("Milk", 2)]
    }
    cost_data = {
        "Flour": 0.5,
        "Egg": 0.2,
        "Milk": 1.0
    }
    expected = {'Pancake': 2.6, 'Omelette': 1.4}
    assert calculate_total_cost(recipe_data, cost_data) == expected

def test_missing_cost_data_raises_error():
    recipe_data = {
        "Salad": [("Lettuce", 1), ("Tomato", 2), ("Cucumber", 1)]
    }
    cost_data = {
        "Lettuce": 1.5,
        "Tomato": 0.8
    }
    with pytest.raises(ValueError, match="Cost information missing for: Cucumber"):
        calculate_total_cost(recipe_data, cost_data)

def test_partial_cost_data():
    recipe_data = {
        "Burger": [("Bun", 2), ("Patty", 1), ("Cheese", 1)]
    }
    cost_data = {
        "Bun": 0.3,
        "Cheese": 0.5
    }
    with pytest.raises(ValueError, match="Cost information missing for: Patty"):
        calculate_total_cost(recipe_data, cost_data)

def test_empty_recipe_data():
    recipe_data = {}
    cost_data = {
        "Flour": 0.5,
        "Egg": 0.2,
        "Milk": 1.0
    }
    assert calculate_total_cost(recipe_data, cost_data) == {}

def test_empty_cost_data():
    recipe_data = {
        "Bread": [("Flour", 1), ("Water", 1)]
    }
    cost_data = {}
    with pytest.raises(ValueError, match="Cost information missing for: Flour"):
        calculate_total_cost(recipe_data, cost_data)