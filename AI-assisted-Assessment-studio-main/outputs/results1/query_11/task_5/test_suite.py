import pytest
from solution import ingredient_converter

@pytest.mark.parametrize("recipe, conversion_factor, expected", [
    (['2 cups flour'], 2, ['4.0 cups flour']),
    (['3 tbsp sugar', '1.5 liters milk'], 0.5, ['1.5 tbsp sugar', '0.75 liters milk']),
    (['5 grams salt', '2 tsp vanilla'], 0.1, ['0.5 grams salt', '0.2 tsp vanilla']),
    (['10 kg potatoes'], 3, ['30.0 kg potatoes']),
    (['1.25 oz chocolate', '0.5 cups butter'], 10, ['12.5 oz chocolate', '5.0 cups butter'])
])
def test_ingredient_converter(recipe, conversion_factor, expected):
    assert ingredient_converter(recipe, conversion_factor) == expected
