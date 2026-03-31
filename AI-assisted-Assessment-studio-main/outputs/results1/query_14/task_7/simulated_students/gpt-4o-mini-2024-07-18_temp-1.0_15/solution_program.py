def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split quantity into the number and the unit
        number, unit = quantity.split(' ', 1)
        # Convert number to integer and multiply
        new_number = round(int(number) * multiplier)
        # Store the new quantity in the new dictionary
        new_recipe[ingredient] = f'{new_number} {unit}'
    return new_recipe