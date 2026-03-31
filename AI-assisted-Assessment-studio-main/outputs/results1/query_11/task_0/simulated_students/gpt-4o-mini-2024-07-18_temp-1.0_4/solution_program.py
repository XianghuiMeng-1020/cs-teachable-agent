def calculate_ingredients(recipe_list, recipe_name):
    for recipe in recipe_list:
        if recipe[0] == recipe_name:
            return recipe[1]
    return []