def ingredient_substitutes(recipe, substitutes):
    result = {}
    for ingredient, quantity in recipe.items():
        if ingredient in substitutes:
            result[substitutes[ingredient]] = quantity
        else:
            result[ingredient] = quantity
    return result