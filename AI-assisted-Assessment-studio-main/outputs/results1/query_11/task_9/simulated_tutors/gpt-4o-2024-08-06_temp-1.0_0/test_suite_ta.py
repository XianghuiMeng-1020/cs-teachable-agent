from program import *
import pytest
from program import calculate_total_cost

@pytest.mark.parametrize("recipe_ingredients, ingredient_prices, expected_total", [
    (['flour:2,sugar:1','milk:3'],'flour:0.5,sugar:0.2,milk:1.0', 4.4),
    (['rice:3,chicken:2','salt:1,pepper:1'],'rice:1.0,chicken:2.5,salt:0.3,pepper:0.4', 9.4),
    (['eggs:6','bacon:2'],'eggs:0.4,bacon:1.5', 4.9),
    (['sugar:2,cocoa:1,milk:1'],'sugar:0.5,cocoa:1.0,milk:0.8', 3.3),
    (['flour:3,butter:2','butter:1','sugar:1'],'flour:0.6,butter:2.0,sugar:0.7', 8.5)
])
def test_calculate_total_cost(recipe_ingredients, ingredient_prices, expected_total):
    assert calculate_total_cost(recipe_ingredients, ingredient_prices) == expected_total
