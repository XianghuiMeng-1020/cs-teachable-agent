import os

def get_recipes_by_category(filename, category_name):
    if not os.path.isfile(filename):
        return []

    recipes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  
                    parts = line.split(';')
                    if len(parts) == 4:
                        recipe_name = parts[0].strip()
                        ingredients = parts[1].strip()  
                        preparation_time = parts[2].strip()  
                        category = parts[3].strip()
                        if category.lower() == category_name.lower():
                            recipes.append(recipe_name)
    except Exception:
        return []

    return recipes

# Test suite

def test_get_recipes_by_category():
    # Test case: Valid file, valid category
    with open('test_recipes.txt', 'w') as f:
        f.write("Pasta; pasta, tomato, cheese; 20 min; main course\n")
        f.write("Salad; lettuce, tomato; 10 min; appetizer\n")
        f.write("Cake; sugar, flour, butter; 60 min; dessert\n")
    assert get_recipes_by_category('test_recipes.txt', 'main course') == ['Pasta']

    # Test case: File does not exist
    assert get_recipes_by_category('nonexistent_file.txt', 'main course') == []

    # Test case: Category with no recipes
    assert get_recipes_by_category('test_recipes.txt', 'snack') == []

    # Test case: Invalid line format
    with open('test_recipes_invalid.txt', 'w') as f:
        f.write("Pasta; pasta, tomato, cheese; 20 min\n")  # Missing category
        f.write("Salad; lettuce, tomato; 10 min; appetizer\n")
    assert get_recipes_by_category('test_recipes_invalid.txt', 'main course') == []

    # Test case: Empty file
    with open('empty_recipes.txt', 'w') as f:
        pass  # Just create an empty file
    assert get_recipes_by_category('empty_recipes.txt', 'main course') == []

    print('All tests passed!')

test_get_recipes_by_category()