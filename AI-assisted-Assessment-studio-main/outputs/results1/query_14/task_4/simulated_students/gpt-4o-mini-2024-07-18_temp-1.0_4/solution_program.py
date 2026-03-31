def ingredient_quantifier(recipe):
    if not recipe:
        return "The recipe requires no ingredients."
    ingredients = []
    for ingredient, quantity in recipe.items():
        ingredients.append(f"{quantity} of {ingredient}")
    ingredients_str = ', '.join(ingredients)
    return f"To make this recipe, you will need: {ingredients_str}."