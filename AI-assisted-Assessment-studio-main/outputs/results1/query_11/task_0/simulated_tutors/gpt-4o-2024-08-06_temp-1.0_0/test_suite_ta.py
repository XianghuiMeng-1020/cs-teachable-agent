from program import *
import pytest

from program import calculate_ingredients

def test_known_recipe():
    recipes = [
        ("Pasta", [("Flour", 100), ("Egg", 2), ("Salt", 1)]),
        ("Omelette", [("Egg", 3), ("Salt", 1), ("Oil", 1)]),
        ("Cake", [("Flour", 200), ("Egg", 3), ("Sugar", 100), ("Salt", 1)])
    ]
    
    result = calculate_ingredients(recipes, "Cake")
    assert result == [("Flour", 200), ("Egg", 3), ("Sugar", 100), ("Salt", 1)]

def test_nonexistent_recipe():
    recipes = [
        ("Pasta", [("Flour", 100), ("Egg", 2), ("Salt", 1)]),
        ("Omelette", [("Egg", 3), ("Salt", 1), ("Oil", 1)])
    ]
    
    result = calculate_ingredients(recipes, "Bread")
    assert result == []

def test_empty_result_for_empty_list():
    recipes = []
    
    result = calculate_ingredients(recipes, "Cake")
    assert result == []

def test_case_sensitivity():
    recipes = [
        ("cake", [("Flour", 200), ("Egg", 3), ("Sugar", 100), ("Salt", 1)])
    ]
    
    result = calculate_ingredients(recipes, "Cake")
    assert result == []

def test_multiple_same_ingredient():
    recipes = [
        ("Omlette Special", [("Egg", 3), ("Salt", 1), ("Salt", 2)])
    ]
    
    result = calculate_ingredients(recipes, "Omlette Special")
    assert result == [("Egg", 3), ("Salt", 3)]