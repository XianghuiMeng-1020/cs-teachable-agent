import os

def get_recipes_by_category(filename, category_name):
    if not os.path.isfile(filename):
        return []

    recipes = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                parts = line.strip().split(';')
                if len(parts) != 4:
                    continue  # skip lines that don't have 4 parts
                recipe_name, ingredients, prep_time, category = parts
                if category.strip().lower() == category_name.strip().lower():
                    recipes.append(recipe_name.strip())
            except Exception:
                continue  # skip any malformed lines
    return recipes

# Test suite for the get_recipes_by_category function

def test_get_recipes_by_category():
    import tempfile

    # Test 1: Test with valid entries in file
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
        f.write('Pasta Carbonara;Pasta, Eggs, Cheese, Bacon;20;main course\n')
        f.write('Caesar Salad;Lettuce, Croutons, Caesar Dressing;10;appetizer\n')
        f.write('Chocolate Cake;Flour, Chocolate, Sugar, Eggs;60;dessert\n')
    assert get_recipes_by_category(f.name, 'main course') == ['Pasta Carbonara']
    os.remove(f.name)

    # Test 2: Test with no entries for the given category
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
        f.write('Garlic Bread;Bread, Garlic, Butter;5;appetizer\n')
    assert get_recipes_by_category(f.name, 'main course') == []
    os.remove(f.name)

    # Test 3: Test with malformed lines
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
        f.write('Valid Recipe;Ingredient1, Ingredient2;30;main course\n')
        f.write('Invalid Recipe Format\n')
        f.write('Another Valid Recipe;Ingredient3;15;appetizer\n')# Missing category\n')
    assert get_recipes_by_category(f.name, 'main course') == ['Valid Recipe']
    os.remove(f.name)

    # Test 4: Test with non-existent file
    assert get_recipes_by_category('non_existent_file.txt', 'main course') == []

    print('All tests passed!')