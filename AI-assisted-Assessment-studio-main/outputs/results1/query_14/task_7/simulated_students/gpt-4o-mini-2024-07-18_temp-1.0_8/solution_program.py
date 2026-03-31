def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split quantity and unit
        qty, unit = quantity.split(' ', 1)
        # Multiply quantity by the multiplier and round to nearest whole number
        new_qty = round(int(qty) * multiplier)
        # Form the new quantity string
        new_recipe[ingredient] = f'{new_qty} {unit}'
    return new_recipe