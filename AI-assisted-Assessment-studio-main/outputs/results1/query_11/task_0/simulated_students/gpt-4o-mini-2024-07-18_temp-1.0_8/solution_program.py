def calculate_ingredients(recipe_list, recipe_name):
    for name, ingredients in recipe_list:
        if name == recipe_name:
            return ingredients
    return []