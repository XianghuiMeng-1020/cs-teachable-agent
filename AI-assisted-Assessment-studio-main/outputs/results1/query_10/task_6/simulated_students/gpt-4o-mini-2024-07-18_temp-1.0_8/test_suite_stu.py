from solution_program import *
import pytest
import os
from solution_program import RecipeManager

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    with open('recipes.txt', 'w') as f:
        f.write("Simple Cake\nFlour, Sugar, Eggs\nMix ingredients and bake\n\n")

    yield
    
    if os.path.exists('recipes.txt'):
        os.remove('recipes.txt')

def test_add_new_recipe():
    rm = RecipeManager()
    rm.add_recipe("Chocolate Cake", "Cocoa, Sugar, Milk", "Mix and bake")
    rm.add_recipe("Pancakes", "Flour, Milk, Eggs", "Mix and cook")
    with open('recipes.txt', 'r') as f:
        content = f.read()
    assert "Chocolate Cake" in content
    assert "Pancakes" in content
    
def test_get_existing_recipe():
    rm = RecipeManager()
    recipe = rm.get_recipe("Simple Cake")
    assert recipe == ("Flour, Sugar, Eggs", "Mix ingredients and bake")

def test_get_nonexistent_recipe():
    rm = RecipeManager()
    recipe = rm.get_recipe("Nonexistent Cake")
    assert recipe is None

    
def test_remove_existing_recipe():
    rm = RecipeManager()
    result = rm.remove_recipe("Simple Cake")
    with open('recipes.txt', 'r') as f:
        content = f.read()
    assert result is True
    assert "Simple Cake" not in content
    
def test_remove_nonexistent_recipe():
    rm = RecipeManager()
    result = rm.remove_recipe("Imaginary Cake")
    assert result is False

def test_add_duplicate_recipe():
    rm = RecipeManager()
    with pytest.raises(Exception, match="already exists"):
        rm.add_recipe("Simple Cake", "Flour, Sugar", "Mix and bake")