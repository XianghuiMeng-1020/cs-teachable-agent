from program import *
import pytest
from program import suggest_recipe


def test_exact_budget():
    budget = 10
    recipes = ["Pasta:5,5", "Salad:3,2,1,4", "Soup:6,3", "Sandwich:5,5"]
    assert suggest_recipe(budget, recipes) == "Pasta"

def test_no_recipe_within_budget():
    budget = 3
    recipes = ["Pizza:5,8", "Burger:6,9"]
    assert suggest_recipe(budget, recipes) == "No recipe available"

def test_one_recipe_within_budget():
    budget = 18
    recipes = ["Cake:5,9,6", "Pie:8,6,5", "Cookies:12,6"]
    assert suggest_recipe(budget, recipes) == "Pie"

def test_multiple_recipes_within_budget():
    budget = 15
    recipes = ["Ice Cream:7,7", "Brownies:5,5,5", "Pudding:6,4,2", "Fruit Salad:4,4,3,2"]
    assert suggest_recipe(budget, recipes) == "Brownies"

def test_tie_on_costs():
    budget = 9
    recipes = ["Chips:4,5", "Dip:3,3,3", "Biscotti:9"]
    assert suggest_recipe(budget, recipes) == "Chips"
