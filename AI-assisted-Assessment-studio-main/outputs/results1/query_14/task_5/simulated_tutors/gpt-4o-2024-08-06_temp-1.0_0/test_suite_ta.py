from program import *
import pytest
from program import parse_ingredient_list

@pytest.mark.parametrize("test_input,expected", [
    ("flour,200,grams; sugar,100,grams; eggs,3,units", {
        'flour': {'quantity': '200', 'unit': 'grams'},
        'sugar': {'quantity': '100', 'unit': 'grams'},
        'eggs': {'quantity': '3', 'unit': 'units'}
    }),
    ("milk,500,ml", {
        'milk': {'quantity': '500', 'unit': 'ml'}
    }),
    ("chocolate,100,grams; butter,250,grams", {
        'chocolate': {'quantity': '100', 'unit': 'grams'},
        'butter': {'quantity': '250', 'unit': 'grams'}
    }),
    ("rice,2,cups; water,500,ml", {
        'rice': {'quantity': '2', 'unit': 'cups'},
        'water': {'quantity': '500', 'unit': 'ml'}
    }),
    ("eggplant,150,grams; olive oil,50,ml; garlic,3,cloves", {
        'eggplant': {'quantity': '150', 'unit': 'grams'},
        'olive oil': {'quantity': '50', 'unit': 'ml'},
        'garlic': {'quantity': '3', 'unit': 'cloves'}
    }),
])
def test_parse_ingredient_list(test_input, expected):
    assert parse_ingredient_list(test_input) == expected
