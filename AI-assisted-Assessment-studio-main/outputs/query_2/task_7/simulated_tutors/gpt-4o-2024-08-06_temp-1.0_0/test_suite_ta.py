from program import *
import pytest
import os
from program import parse_recipe_ingredients


def setup_module(module):
    with open('recipes.txt', 'w') as f:
        f.write("""
Recipe: Pancakes
Ingredients:
- 1 cup flour
- 2 tablespoons sugar
- 1 teaspoon baking powder
- 1/2 teaspoon salt
- 1 egg
- 1 cup milk
- 2 tablespoons melted butter

Recipe: Omelette
Ingredients:
- 2 eggs
- 1/4 cup milk
- Salt and pepper to taste
- 1 tablespoon butter

Recipe: Pizza
Ingredients:
- 2 cups flour
- 1 teaspoon yeast
- 1 cup water
- 1/4 cup tomato sauce
- 100g mozzarella cheese
- 10 slices pepperoni

""")


def teardown_module(module):
    os.remove('recipes.txt')


def test_single_recipe():
    with open('single_recipe.txt', 'w') as f:
        f.write("""
Recipe: Cookies
Ingredients:
- 2 cups flour
- 1 cup sugar
- 1 teaspoon vanilla extract
- 1/2 teaspoon baking soda
- 1 egg
- 1/2 cup butter

""")
    result = parse_recipe_ingredients('single_recipe.txt')
    assert result == {"Cookies": ["2 cups flour", "1 cup sugar", "1 teaspoon vanilla extract", "1/2 teaspoon baking soda", "1 egg", "1/2 cup butter"]}
    os.remove('single_recipe.txt')


def test_different_structure_order():
    with open('different_structure.txt', 'w') as f:
        f.write("""
Recipe: Salad
Ingredients:
- 1 cup lettuce
- 1/2 cup tomato
- 1/4 cup cucumber
- 2 tablespoons olive oil
- Salt to taste

""")
    result = parse_recipe_ingredients('different_structure.txt')
    assert result == {"Salad": ["1 cup lettuce", "1/2 cup tomato", "1/4 cup cucumber", "2 tablespoons olive oil", "Salt to taste"]}
    os.remove('different_structure.txt')


def test_multiple_recipes():
    result = parse_recipe_ingredients('recipes.txt')
    expected = {
        "Pancakes": [
            "1 cup flour",
            "2 tablespoons sugar",
            "1 teaspoon baking powder",
            "1/2 teaspoon salt",
            "1 egg",
            "1 cup milk",
            "2 tablespoons melted butter"
        ],
        "Omelette": [
            "2 eggs",
            "1/4 cup milk",
            "Salt and pepper to taste",
            "1 tablespoon butter"
        ],
        "Pizza": [
            "2 cups flour",
            "1 teaspoon yeast",
            "1 cup water",
            "1/4 cup tomato sauce",
            "100g mozzarella cheese",
            "10 slices pepperoni"
        ]
    }
    assert result == expected


def test_large_recipe():
    with open('large_recipe.txt', 'w') as f:
        f.write("""
Recipe: Big Feast
Ingredients:
- 5 lbs chicken
- 4 cups rice
- 3 cups vegetables
- 2 liters broth
- ½ cup soy sauce
- Salt and pepper

""")
    result = parse_recipe_ingredients('large_recipe.txt')
    assert result == {
        "Big Feast": [
            "5 lbs chicken",
            "4 cups rice",
            "3 cups vegetables",
            "2 liters broth",
            "½ cup soy sauce",
            "Salt and pepper"
        ]
    }
    os.remove('large_recipe.txt')


def test_no_ingredients():
    with open('no_ingredients.txt', 'w') as f:
        f.write("""
Recipe: Empty Dish
Ingredients:

""")
    result = parse_recipe_ingredients('no_ingredients.txt')
    assert result == {"Empty Dish": []}
    os.remove('no_ingredients.txt')
