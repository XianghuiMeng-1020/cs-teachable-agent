def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split the quantity from its unit
        qty, unit = quantity.split(' ', 1)
        # Convert quantity to integer and multiply by multiplier
        new_qty = round(int(qty) * multiplier)
        # Create the new entry in the new recipe dictionary
        new_recipe[ingredient] = f'{new_qty} {unit}'
    return new_recipe