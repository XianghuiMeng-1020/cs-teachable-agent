def ingredient_substitutes(recipe, substitutes):
    return {substitutes.get(ingredient, ingredient): quantity for ingredient, quantity in recipe.items() }