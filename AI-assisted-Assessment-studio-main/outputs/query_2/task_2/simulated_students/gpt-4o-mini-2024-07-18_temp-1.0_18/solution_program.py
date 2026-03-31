import os


def get_recipes_by_category(filename, category_name):
    if not os.path.isfile(filename):
        return []

    recipes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                fields = line.strip().split(';')
                if len(fields) != 4:
                    continue
                recipe_name, ingredients, prep_time, category = fields
                if category.strip().lower() == category_name.strip().lower():
                    recipes.append(recipe_name.strip())
    except Exception:
        return []

    return recipes

# Test Suite

def test_get_recipes_by_category():
    # Prepare test files
    test_filename = 'recipes.txt'
    with open(test_filename, 'w') as f:
        f.write('Pasta;noodles,tomato sauce;15 minutes;main course\n')
        f.write('Salad;lettuce,tomato;10 minutes;appetizer\n')
        f.write('Cake;flour,sugar;30 minutes;dessert\n')
        f.write('Omelette;eggs;5 minutes;breakfast\n')
        f.write('InvalidRecipe;invalid;format;\n')

    assert get_recipes_by_category(test_filename, 'main course') == ['Pasta']
    assert get_recipes_by_category(test_filename, 'appetizer') == ['Salad']
    assert get_recipes_by_category(test_filename, 'dessert') == ['Cake']
    assert get_recipes_by_category(test_filename, 'breakfast') == ['Omelette']
    assert get_recipes_by_category(test_filename, 'snack') == []
    assert get_recipes_by_category('invalid_file.txt', 'main course') == []
    assert get_recipes_by_category(test_filename, '') == []
    assert get_recipes_by_category(test_filename, 'appetizer') == ['Salad']
    assert get_recipes_by_category(test_filename, 'main course') == ['Pasta']
    assert get_recipes_by_category(test_filename, 'invalid category') == []

    print("All tests passed!")

# Run tests

test_get_recipes_by_category()