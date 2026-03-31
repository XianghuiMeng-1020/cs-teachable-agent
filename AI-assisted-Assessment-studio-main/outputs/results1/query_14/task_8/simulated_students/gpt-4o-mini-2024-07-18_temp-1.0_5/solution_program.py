def get_ingredient_quantity(recipe, ingredient):
    if ingredient in recipe:
        return recipe[ingredient]
    return 'Ingredient not found'