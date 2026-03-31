def ingredient_substitutes(recipe, substitutes):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        if ingredient in substitutes:
            new_recipe[substitutes[ingredient]] = quantity
        else:
            new_recipe[ingredient] = quantity
    return new_recipe