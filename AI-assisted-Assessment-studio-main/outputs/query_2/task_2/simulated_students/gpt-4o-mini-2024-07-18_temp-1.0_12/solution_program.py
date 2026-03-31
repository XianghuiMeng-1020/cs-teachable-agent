import os


def get_recipes_by_category(filename, category_name):
    if not os.path.isfile(filename):
        return []

    recipes = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) != 4:
                continue
            recipe_name, ingredients, prep_time, category = parts
            if category.strip().lower() == category_name.strip().lower():
                recipes.append(recipe_name.strip())
    return recipes


def test_get_recipes_by_category():
    # Test 1: Test with a valid file and valid category
    with open('test_recipes.txt', 'w') as f:
        f.write('Pasta;flour, eggs;30 minutes;main course\n')
        f.write('Salad;lettuce, tomato;15 minutes;appetizer\n')
        f.write('Cake;flour, sugar;60 minutes;dessert\n')

    assert get_recipes_by_category('test_recipes.txt', 'main course') == ['Pasta']

    # Test 2: Test with a valid file but category with no recipes
    assert get_recipes_by_category('test_recipes.txt', 'snack') == []

    # Test 3: Test with a non-existent file
    assert get_recipes_by_category('non_existent.txt', 'main course') == []

    # Test 4: Test with a file that has invalid formatting
    with open('invalid_recipes.txt', 'w') as f:
        f.write('Pasta;flour, eggs;30 minutes\n')
        f.write('Salad;lettuce, tomato;15 minutes;appetizer\n')

    assert get_recipes_by_category('invalid_recipes.txt', 'appetizer') == ['Salad']
    assert get_recipes_by_category('invalid_recipes.txt', 'main course') == []

    # Test 5: Test an empty file
    with open('empty.txt', 'w') as f:
        pass

    assert get_recipes_by_category('empty.txt', 'main course') == []

    # Clean up test files
    os.remove('test_recipes.txt')
    os.remove('invalid_recipes.txt')
    os.remove('empty.txt')


test_get_recipes_by_category()