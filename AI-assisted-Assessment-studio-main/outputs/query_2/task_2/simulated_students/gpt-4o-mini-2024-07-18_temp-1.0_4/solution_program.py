import os

def get_recipes_by_category(filename, category_name):
    if not os.path.isfile(filename):
        return []
    
    recipes = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(';')
            if len(parts) != 4:
                continue

            recipe_name = parts[0].strip()
            ingredients = parts[1].strip()
            preparation_time = parts[2].strip()
            category = parts[3].strip()

            if category.lower() == category_name.lower():
                recipes.append(recipe_name)
    
    return recipes


def test_get_recipes_by_category():
    # Creating a temporary file to test the function
    test_filename = 'test_recipes.txt'
    with open(test_filename, 'w') as test_file:
        test_file.write('Spaghetti Bolognese;spaghetti, ground beef, tomato sauce;30 minutes;main course\n')
        test_file.write('Caesar Salad;romaine, chicken, croutons, parmesan;15 minutes;appetizer\n')
        test_file.write('Chocolate Cake;flour, sugar, cocoa powder;60 minutes;dessert\n')
        test_file.write('Invalid Recipe Line Without Enough Fields\n')

    # Test cases
    assert get_recipes_by_category(test_filename, 'main course') == ['Spaghetti Bolognese']
    assert get_recipes_by_category(test_filename, 'appetizer') == ['Caesar Salad']
    assert get_recipes_by_category(test_filename, 'dessert') == ['Chocolate Cake']
    assert get_recipes_by_category(test_filename, 'snack') == []
    assert get_recipes_by_category(test_filename, 'main course ') == ['Spaghetti Bolognese']
    assert get_recipes_by_category('nonexistent_file.txt', 'appetizer') == []
    assert get_recipes_by_category(test_filename, '') == []

    print('All tests passed!')


# Uncomment the line below to run the tests
# test_get_recipes_by_category()