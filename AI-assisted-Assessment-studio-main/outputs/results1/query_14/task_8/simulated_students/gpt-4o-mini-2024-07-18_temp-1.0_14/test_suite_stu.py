from solution_program import *
import pytest

from solution_program import get_ingredient_quantity

def test_get_ingredient_quantity():
    recipe = {"flour": "2 cups", "sugar": "1 cup", "butter": "100g"}
    assert get_ingredient_quantity(recipe, "sugar") == "1 cup"

    assert get_ingredient_quantity(recipe, "flour") == "2 cups"
    
    assert get_ingredient_quantity(recipe, "butter") == "100g"

    assert get_ingredient_quantity(recipe, "salt") == "Ingredient not found"

    assert get_ingredient_quantity({}, "sugar") == "Ingredient not found"
