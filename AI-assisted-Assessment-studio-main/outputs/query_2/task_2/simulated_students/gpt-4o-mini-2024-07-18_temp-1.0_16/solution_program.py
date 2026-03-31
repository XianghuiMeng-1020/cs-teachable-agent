import os


def get_recipes_by_category(filename, category_name):
    recipes = []
    if not os.path.isfile(filename):
        return recipes
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  
            # Skip empty lines or corrupted lines
            if not line:
                continue
            fields = line.split(';')
            if len(fields) != 4:
                continue  
            recipe_name, ingredients, preparation_time, category = fields
            if category.strip().lower() == category_name.strip().lower():
                recipes.append(recipe_name.strip())
    
    return recipes


def test_get_recipes_by_category():
    # Create sample data
    with open('test_recipes.txt', 'w', encoding='utf-8') as f:
        f.write('Pasta;spaghetti, tomato sauce;30 minutes;main course\n')
        f.write('Salad;lettuce, tomato;10 minutes;appetizer\n')
        f.write('Cheesecake;cream cheese, sugar;60 minutes;dessert\n')
        f.write('Invalid Line\n')
        f.write('Cupcake;flour, sugar, eggs;45 minutes;dessert\n')

    # Test cases
    assert get_recipes_by_category('test_recipes.txt', 'main course') == ['Pasta']
    assert get_recipes_by_category('test_recipes.txt', 'appetizer') == ['Salad']
    assert get_recipes_by_category('test_recipes.txt', 'dessert') == ['Cheesecake', 'Cupcake']
    assert get_recipes_by_category('test_recipes.txt', 'snack') == []
    assert get_recipes_by_category('non_existent_file.txt', 'dessert') == []
    assert get_recipes_by_category('test_recipes.txt', '') == []
    assert get_recipes_by_category('test_recipes.txt', '   DESSERT   ') == ['Cheesecake', 'Cupcake']

    # Clean up
    os.remove('test_recipes.txt')


test_get_recipes_by_category()