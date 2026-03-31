def ingredient_quantifier(recipe):
    if not recipe:
        return "The recipe requires no ingredients."
    ingredients_list = []
    for ingredient, quantity in recipe.items():
        ingredients_list.append(f"{quantity} of {ingredient}")
    ingredients_str = ', '.join(ingredients_list)
    return f"To make this recipe, you will need: {ingredients_str}."