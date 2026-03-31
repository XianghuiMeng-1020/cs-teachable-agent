def ingredient_quantifier(recipe):
    if not recipe:
        return "The recipe requires no ingredients."
    ingredients = []
    for ingredient, quantity in recipe.items():
        ingredients.append(f"{quantity} of {ingredient}")
    return "To make this recipe, you will need: " + ", ".join(ingredients) + "."