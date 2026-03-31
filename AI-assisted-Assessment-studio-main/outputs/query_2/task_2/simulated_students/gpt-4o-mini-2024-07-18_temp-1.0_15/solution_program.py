def get_recipes_by_category(filename, category_name):
    import os

    if not os.path.isfile(filename):
        return []

    recipes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(';')
                if len(parts) != 4:
                    continue  # Skip lines that do not have exactly 4 fields

                recipe_name, ingredients, preparation_time, category = parts
                if category.strip().lower() == category_name.strip().lower():
                    recipes.append(recipe_name.strip())
    except Exception as e:
        return []

    return recipes

# Test suite

def test_get_recipes_by_category():
    # Creating test files
    with open('test_recipes.txt', 'w') as f:
        f.write('Pasta;Noodles, Cheese, Tomato Sauce;30 minutes;main course\n')
        f.write('Salad;Lettuce, Tomato, Cucumber;15 minutes;appetizer\n')
        f.write('Cake;Flour, Sugar, Eggs;60 minutes;dessert\n')
        f.write('Invalid Recipe Line\n')  # Invalid line
        f.write('Soup;Water, Vegetables;20 minutes;appetizer\n')

    assert get_recipes_by_category('test_recipes.txt', 'main course') == ['Pasta']
    assert get_recipes_by_category('test_recipes.txt', 'appetizer') == ['Salad', 'Soup']
    assert get_recipes_by_category('test_recipes.txt', 'dessert') == ['Cake']
    assert get_recipes_by_category('test_recipes.txt', 'snack') == []
    assert get_recipes_by_category('invalid_file.txt', 'main course') == []  # Invalid file
    assert get_recipes_by_category('test_recipes.txt', '') == []  # Empty category

    print('All tests passed!')

test_get_recipes_by_category()