import os


def get_recipes_by_category(filename, category_name):
    if not os.path.isfile(filename):
        return []

    recipes = []

    with open(filename, 'r') as file:
        for line in file:
            fields = line.strip().split(';')
            if len(fields) != 4:
                continue  # Skip lines with an unexpected format
            recipe_name = fields[0].strip()
            ingredients = fields[1].strip()
            prep_time = fields[2].strip()
            category = fields[3].strip()

            if category.lower() == category_name.lower():
                recipes.append(recipe_name)

    return recipes


def test_get_recipes_by_category():
    # Create a temporary recipe file for testing
    test_filename = 'test_recipes.txt'
    with open(test_filename, 'w') as f:
        f.write('Spaghetti;spaghetti, tomatoes;30;main course\n')
        f.write('Caesar Salad;lettuce, chicken;20;appetizer\n')
        f.write('Cheesecake;cream cheese, sugar;60;dessert\n')
        f.write('Invalid Recipe Line\n')  # This line is invalid

    assert get_recipes_by_category(test_filename, 'main course') == ['Spaghetti']
    assert get_recipes_by_category(test_filename, 'appetizer') == ['Caesar Salad']
    assert get_recipes_by_category(test_filename, 'dessert') == ['Cheesecake']
    assert get_recipes_by_category(test_filename, 'snack') == []
    assert get_recipes_by_category('non_existing_file.txt', 'main course') == []
    assert get_recipes_by_category(test_filename, '') == []

    # Clean up the test file
    os.remove(test_filename)


test_get_recipes_by_category()