import os


def get_recipes_by_category(filename, category_name):
    if not os.path.isfile(filename):
        return []
    
    recipes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(';')
                if len(parts) != 4:
                    continue
                recipe_name, ingredients, preparation_time, category = parts
                if category.strip().lower() == category_name.strip().lower():
                    recipes.append(recipe_name.strip())
    except Exception:
        return []
    
    return recipes


def test_get_recipes_by_category():
    # Create a temporary file for testing
    test_filename = 'test_recipes.txt'
    with open(test_filename, 'w') as f:
        f.write('Pasta;Noodles, Sauce;30 minutes;Main Course\n')
        f.write('Salad;Lettuce, Tomatoes;15 minutes;Appetizer\n')
        f.write('Cheesecake;Cheese, Sugar;60 minutes;Dessert\n')
        f.write('Bread;Flour, Water;120 minutes;Main Course\n')
        f.write('InvalidRecipe;OnlyOneField\n')

    assert get_recipes_by_category(test_filename, 'main course') == ['Pasta', 'Bread']
    assert get_recipes_by_category(test_filename, 'appetizer') == ['Salad']
    assert get_recipes_by_category(test_filename, 'dessert') == ['Cheesecake']
    assert get_recipes_by_category(test_filename, 'snack') == []
    assert get_recipes_by_category('non_existing_file.txt', 'appetizer') == []
    assert get_recipes_by_category(test_filename, '') == []
    assert get_recipes_by_category(test_filename, 'main course ') == ['Pasta', 'Bread']
    
    os.remove(test_filename)


test_get_recipes_by_category()