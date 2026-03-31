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
