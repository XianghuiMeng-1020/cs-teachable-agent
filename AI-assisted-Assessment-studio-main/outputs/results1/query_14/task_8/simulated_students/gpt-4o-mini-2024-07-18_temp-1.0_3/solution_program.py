def get_ingredient_quantity(recipe, ingredient):
    if ingredient in recipe:
        return recipe[ingredient]
    else:
        return "Ingredient not found"