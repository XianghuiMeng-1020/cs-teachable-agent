import os


def get_recipes_by_category(filename, category_name):
    if not os.path.exists(filename):
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
            recipe_name, ingredients, prep_time, category = parts
            if category.strip().lower() == category_name.strip().lower():
                recipes.append(recipe_name.strip())

    return recipes


def test_get_recipes_by_category():
    # Test with valid file and category
    with open('test_recipes.txt', 'w') as f:
        f.write('Pasta;Noodles, Tomato Sauce;30 minutes;main course\n')
        f.write('Salad;Lettuce, Tomato;15 minutes;appetizer\n')
        f.write('Cake;Flour, Eggs;60 minutes;dessert\n')
    assert get_recipes_by_category('test_recipes.txt', 'main course') == ['Pasta']
    assert get_recipes_by_category('test_recipes.txt', 'appetizer') == ['Salad']
    assert get_recipes_by_category('test_recipes.txt', 'dessert') == ['Cake']

    # Test with category that has no recipes
    assert get_recipes_by_category('test_recipes.txt', 'snacks') == []

    # Test with non-existent file
    assert get_recipes_by_category('non_existent_file.txt', 'main course') == []

    # Test with invalid line format
    with open('invalid_recipes.txt', 'w') as f:
        f.write('InvalidRecipe;JustOneField\n')
        f.write('AnotherInvalidRecipe;Ingredient1;Ingredient2;Ingredient3;;\n')
    assert get_recipes_by_category('invalid_recipes.txt', 'main course') == []

    # Test with empty file
    open('empty_recipes.txt', 'w').close()
    assert get_recipes_by_category('empty_recipes.txt', 'main course') == []


# Run the test suite

test_get_recipes_by_category()