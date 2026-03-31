def ingredient_quantifier(recipe):
    if not recipe:
        return "The recipe requires no ingredients."
    ingredients_list = []
    for ingredient, quantity in recipe.items():
        ingredients_list.append(f"{quantity} of {ingredient}")
    return "To make this recipe, you will need: " + ', '.join(ingredients_list) + '.'