import os


def get_recipes_by_category(filename, category_name):
    recipes = []
    if not os.path.isfile(filename):
        return recipes

    with open(filename, 'r') as file:
        for line in file:
            fields = line.strip().split(';')
            if len(fields) != 4:
                continue  # Skip lines that don't have the correct format
            recipe_name, ingredients, prep_time, category = fields
            if category.strip().lower() == category_name.strip().lower():
                recipes.append(recipe_name.strip())

    return recipes
