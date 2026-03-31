from solution_program import *
import pytest

from solution_program import ingredient_substitutes

def test_simple_substitution():
    recipe = {'sugar': '1 cup', 'flour': '2 cups', 'butter': '200g'}
    substitutes = {'sugar': 'honey', 'butter': 'margarine'}
    result = ingredient_substitutes(recipe, substitutes)
    assert result == {'honey': '1 cup', 'flour': '2 cups', 'margarine': '200g'}

def test_no_substitution():
    recipe = {'salt': '1 tsp', 'chicken': '500g'}
    substitutes = {'sugar': 'honey', 'butter': 'margarine'}
    result = ingredient_substitutes(recipe, substitutes)
    assert result == {'salt': '1 tsp', 'chicken': '500g'}

def test_all_substituted():
    recipe = {'rice': '1 cup', 'oil': '2 tbsp'}
    substitutes = {'rice': 'quinoa', 'oil': 'coconut oil'}
    result = ingredient_substitutes(recipe, substitutes)
    assert result == {'quinoa': '1 cup', 'coconut oil': '2 tbsp'}

def test_some_non_substituted():
    recipe = {'milk': '1 cup', 'flour': '2 cups', 'eggs': '2 units'}
    substitutes = {'milk': 'almond milk', 'butter': 'margarine'}
    result = ingredient_substitutes(recipe, substitutes)
    assert result == {'almond milk': '1 cup', 'flour': '2 cups', 'eggs': '2 units'}

def test_empty_substitutes():
    recipe = {'coffee': '2 tsp', 'sugar': '1 tsp', 'milk': '100 ml'}
    substitutes = {}
    result = ingredient_substitutes(recipe, substitutes)
    assert result == {'coffee': '2 tsp', 'sugar': '1 tsp', 'milk': '100 ml'}
