import pytest
from solution import ingredient_quantifier

@pytest.mark.parametrize("recipe, expected_output", [
    ({}
     , "The recipe requires no ingredients."),
    ({"flour": "2 cups", "sugar": "1 cup", "butter": "250 grams"},
     "To make this recipe, you will need: 2 cups of flour, 1 cup of sugar, 250 grams of butter"),
    ({"milk": "500 ml", "cocoa": "100 grams", "chocolate": "200 grams", "egg": "2 whole"},
     "To make this recipe, you will need: 500 ml of milk, 100 grams of cocoa, 200 grams of chocolate, 2 whole of egg"),
    ({"rice": "1 kg"},
     "To make this recipe, you will need: 1 kg of rice"),
    ({"olive oil": "1 tablespoon", "lemon juice": "3 tablespoons", "salt": "2 teaspoons"},
     "To make this recipe, you will need: 1 tablespoon of olive oil, 3 tablespoons of lemon juice, 2 teaspoons of salt"),
    ({"water": "litres"},
     "To make this recipe, you will need: litres of water")
])
def test_ingredient_quantifier(recipe, expected_output):
    assert ingredient_quantifier(recipe) == expected_output