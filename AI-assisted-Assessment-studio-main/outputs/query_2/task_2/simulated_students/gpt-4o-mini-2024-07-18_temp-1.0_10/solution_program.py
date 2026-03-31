import os


def get_recipes_by_category(filename, category_name):
    if not os.path.exists(filename):
        return []

    recipes = []
    
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) != 4:
                continue  # Skip lines that do not have the correct format
            recipe_name, ingredients, prep_time, category = parts
            
            if category.strip().lower() == category_name.strip().lower():
                recipes.append(recipe_name.strip())

    return recipes
