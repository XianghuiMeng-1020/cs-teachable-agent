def get_ingredient_quantity(recipe, ingredient):
    return recipe.get(ingredient, 'Ingredient not found')