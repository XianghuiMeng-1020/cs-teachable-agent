import pytest
from solution import get_ingredient_list

def test_ingredients_with_quantities_and_units():
    recipe_text = "2 cups flour\n1/2 teaspoon salt\n1 egg"
    expected_output = {
        "flour": "2 cups",
        "salt": "1/2 teaspoon",
        "egg": "1"
    }
    assert get_ingredient_list(recipe_text) == expected_output

def test_ingredients_without_quantities_or_units():
    recipe_text = "egg\nsugar"
    expected_output = {
        "egg": "",
        "sugar": ""
    }
    assert get_ingredient_list(recipe_text) == expected_output

def test_mixed_format_ingredients():
    recipe_text = "egg\n2 tablespoons sugar\nsalt"
    expected_output = {
        "egg": "",
        "sugar": "2 tablespoons",
        "salt": ""
    }
    assert get_ingredient_list(recipe_text) == expected_output

def test_case_insensitivity():
    recipe_text = "1 Liter Water\n1 liter water\nFlour 100g"
    expected_output = {
        "water": "1 liter",
        "flour": ""
    }
    assert get_ingredient_list(recipe_text) == expected_output

def test_complex_ingredient_names():
    recipe_text = "1 kg chicken breast\n100 ml olive oil\nbasil"
    expected_output = {
        "chicken breast": "1 kg",
        "olive oil": "100 ml",
        "basil": ""
    }
    assert get_ingredient_list(recipe_text) == expected_output
