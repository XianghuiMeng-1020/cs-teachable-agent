import os
import pytest
from solution import generate_shopping_list

recipes_file = 'recipes.txt'
available_file = 'available.txt'
output_file = 'shopping_list.txt'

def setup_module(module):
    with open(recipes_file, 'w') as f:
        f.write('Pasta\nTomato\nBasil\nGarlic\n\nSalad\nLettuce\nTomato\nCucumber\n')

    with open(available_file, 'w') as f:
        f.write('Tomato\nLettuce\nSalt\nOil\n')

def teardown_module(module):
    os.remove(recipes_file)
    os.remove(available_file)
    if os.path.exists(output_file):
        os.remove(output_file)

@pytest.mark.parametrize('test_name, recipes_content, available_content, expected_output', [
    ('test_full_missing_ingredients', 'Pasta\nSpaghetti\nOnions\n\nSoup\nWater\n', 'Salt\nOil\n', 'Spaghetti\nOnions\nWater\n'),
    ('test_some_ingredients_missing', 'Pasta\nTomato\nBasil\nGarlic\n\nSalad\nLettuce\nTomato\nCucumber\n', 'Tomato\nLettuce\nSalt\nOil\n', 'Basil\nGarlic\nCucumber\n'),
    ('test_no_file_overlap', 'Sandwich\nBread\nHam\nCheese\n', 'Pepper\nSalt\n', 'Bread\nHam\nCheese\n'),
    ('test_no_missing_ingredients', 'Soup\nWater\nSalt\n\nPasta\nTomato\nGarlic\n', 'Water\nSalt\nTomato\nGarlic\n', ''),
    ('test_case_insensitive', 'Pizza\nTomato\nMozzarella\nBasil\n', 'tomato\nmozzarella\n', 'Basil\n')
])
def test_generate_shopping_list(test_name, recipes_content, available_content, expected_output):
    with open(recipes_file, 'w') as f:
        f.write(recipes_content)
    with open(available_file, 'w') as f:
        f.write(available_content)
    generate_shopping_list(recipes_file, available_file, output_file)
    with open(output_file, 'r') as f:
        shopping_content = f.read().strip() + '\n'
    assert shopping_content == expected_output