from program import *
import pytest

from program import parse_ingredient_list

@pytest.mark.parametrize("ingredient_string, expected", [
    ("flour:200g;milk:500ml;butter:100g", {"flour": "200g", "milk": "500ml", "butter": "100g"}),
    ("sugar:150g;eggs:2;chocolate:100g", {"sugar": "150g", "eggs": "2", "chocolate": "100g"}),
    ("salt:1tsp;pepper:0.5tsp", {"salt": "1tsp", "pepper": "0.5tsp"}),
    ("olive oil:2tbsp;garlic:3cloves;basil:10leaves", {"olive oil": "2tbsp", "garlic": "3cloves", "basil": "10leaves"}),
    (""