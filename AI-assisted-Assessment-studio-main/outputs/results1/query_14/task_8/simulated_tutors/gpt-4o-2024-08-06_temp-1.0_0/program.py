def get_ingredient_quantity(recipe, ingredient):
    # Check if the ingredient is present in the recipe dictionary
    if ingredient in recipe:
        return recipe[ingredient]
    else:
        return "Ingredient not found"