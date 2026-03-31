def get_recipes_by_category(filename, category_name):
    recipes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(';')
                if len(parts) != 4:
                    continue
                recipe_name, ingredients, preparation_time, category = parts
                if category.lower() == category_name.lower():
                    recipes.append(recipe_name)
    except FileNotFoundError:
        return []
    return recipes

# Test Suite
import unittest
from unittest.mock import mock_open, patch

class TestGetRecipesByCategory(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='Pizza;cheese,tomato;30 minutes;main course\nSalad;lettuce,tomato;cold;appetizer\nCake;flour,eggs;60 minutes;dessert\n')
    def test_valid_category(self, mock_file):
        result = get_recipes_by_category('mock_recipes.txt', 'main course')
        self.assertEqual(result, ['Pizza'])

    @patch('builtins.open', new_callable=mock_open, read_data='Pizza;cheese,tomato;30 minutes;main course\nSalad;lettuce,tomato;cold;appetizer\n')
    def test_no_recipes_in_category(self, mock_file):
        result = get_recipes_by_category('mock_recipes.txt', 'dessert')
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open, read_data='Pizza;cheese,tomato;30 minutes;main course\nInvalid Recipe Line\nSalad;lettuce,tomato;cold;appetizer\n')
    def test_invalid_line(self, mock_file):
        result = get_recipes_by_category('mock_recipes.txt', 'appetizer')
        self.assertEqual(result, ['Salad'])

    def test_file_not_found(self):
        result = get_recipes_by_category('non_existent_file.txt', 'main course')
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_empty_file(self, mock_file):
        result = get_recipes_by_category('mock_recipes.txt', 'main course')
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()