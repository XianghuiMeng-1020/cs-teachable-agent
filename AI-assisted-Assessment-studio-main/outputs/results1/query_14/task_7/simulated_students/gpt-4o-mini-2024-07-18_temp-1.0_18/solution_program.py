def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split quantity and unit
        qty, unit = quantity.split(' ', 1)
        # Convert quantity to integer and multiply
        new_qty = round(int(qty) * multiplier)
        # Create new ingredient entry
        new_recipe[ingredient] = f'{new_qty} {unit}'
    return new_recipe