from program import *
import pytest
import os
from program import read_vegetarian_recipes

sample_input_content = '''
Name: Chicken Curry
Ingredients: chicken, curry powder, onions, garlic

Name: Veggie Stir Fry
Ingredients: broccoli, bell peppers, soy sauce

Name: Beef Stroganoff
Ingredients: beef, mushrooms, sour cream
'''

expected_output_content = '''
Name: Veggie Stir Fry
Ingredients: broccoli, bell peppers, soy sauce
'''

extended_input_content = '''
Name: Chicken Salad
Ingredients: chicken, lettuce, mayonnaise

Name: Mushroom Risotto
Ingredients: rice, mushrooms, parmesan

Name: BBQ Pork Ribs
Ingredients: pork, bbq sauce, spices

Name: Tofu Curry
Ingredients: tofu, curry powder, coconut milk
'''

extended_expected_output_content = '''
Name: Mushroom Risotto
Ingredients: rice, mushrooms, parmesan

Name: Tofu Curry
Ingredients: tofu, curry powder, coconut milk
'''

file_name = "recipes.txt"
output_file_name = "vegetarian_recipes.txt"

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    with open(file_name, 'w') as f:
        f.write(sample_input_content)
    yield
    os.remove(file_name)
    if os.path.exists(output_file_name):
        os.remove(output_file_name)

@pytest.mark.parametrize("file_content, expected_output", [
    (sample_input_content, expected_output_content),
    (extended_input_content, extended_expected_output_content),
    ("\nName: Salad\nIngredients: lettuce, tomato, cucumber\n", "\nName: Salad\nIngredients: lettuce, tomato, cucumber\n"),
    ("\nName: Chicken Roast\nIngredients: chicken, spices\n", ""),
    ("", "")
])
def test_read_vegetarian_recipes(file_content, expected_output):
    with open(file_name, 'w') as f:
        f.write(file_content)
    read_vegetarian_recipes(file_name)
    if expected_output:
        with open(output_file_name, 'r') as f:
            result = f.read()
        assert result == expected_output
    else:
        assert not os.path.exists(output_file_name) or os.stat(output_file_name).st_size == 0