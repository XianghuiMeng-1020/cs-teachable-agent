def ingredient_substitutes(recipe, substitutes):
    new_recipe = {substitutes.get(ingredient, ingredient): quantity for ingredient, quantity in recipe.items()}
    return new_recipe