def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split the quantity from the units
        num, unit = quantity.split(' ', 1)
        # Convert quantity to integer and multiply by the multiplier
        new_quantity = round(int(num) * multiplier)
        # Create the new entry in the recipe dictionary
        new_recipe[ingredient] = f'{new_quantity} {unit}'
    return new_recipe