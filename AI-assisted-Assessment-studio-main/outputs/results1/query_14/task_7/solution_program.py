def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        quantity_parts = quantity.split()
        amount = int(quantity_parts[0])
        unit = ' '.join(quantity_parts[1:])
        new_amount = str(round(amount * multiplier))
        new_recipe[ingredient] = new_amount + ' ' + unit
    return new_recipe
