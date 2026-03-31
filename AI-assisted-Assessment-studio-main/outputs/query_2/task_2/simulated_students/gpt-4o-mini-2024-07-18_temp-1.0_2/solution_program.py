import os


def get_recipes_by_category(filename, category_name):
    if not os.path.exists(filename):
        return []

    recipes = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) != 4:
                continue  # Skip invalid lines
            recipe_name, ingredients, preparation_time, category = parts
            if category.strip().lower() == category_name.strip().lower():
                recipes.append(recipe_name.strip())
    return recipes


def test_get_recipes_by_category():
    # Test case 1: Valid recipes file with categories
    with open('recipes.txt', 'w') as f:
        f.write('Pasta;Pasta, Tomato Sauce;20 minutes;main course\n')
        f.write('Caesar Salad;Lettuce, Croutons, Caesar Dressing;10 minutes;appetizer\n')
        f.write('Chocolate Cake;Flour, Sugar, Cocoa;60 minutes;dessert\n')

    assert get_recipes_by_category('recipes.txt', 'main course') == ['Pasta']
    assert get_recipes_by_category('recipes.txt', 'dessert') == ['Chocolate Cake']
    assert get_recipes_by_category('recipes.txt', 'appetizer') == ['Caesar Salad']

    # Test case 2: Category with no recipes
    assert get_recipes_by_category('recipes.txt', 'snack') == []

    # Test case 3: Non-existing file
    assert get_recipes_by_category('non_existing_file.txt', 'main course') == []

    # Test case 4: Corrupted lines in the file
    with open('corrupted_recipes.txt', 'w') as f:
        f.write('Valid Recipe;Ingredient1, Ingredient2;10;main course\n')
        f.write('Invalid Recipe;Missing;Field\n')

    assert get_recipes_by_category('corrupted_recipes.txt', 'main course') == ['Valid Recipe']
    
    # Test case 5: Empty file
    with open('empty_file.txt', 'w') as f:
        pass  # Just create an empty file
    assert get_recipes_by_category('empty_file.txt', 'main course') == []


test_get_recipes_by_category()