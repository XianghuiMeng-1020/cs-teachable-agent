def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Extract the numerical quantity and the unit of measure
        quantity_value, unit = quantity.split(' ', 1)
        quantity_value = int(quantity_value)
        # Calculate the new quantity and round it
        new_quantity = round(quantity_value * multiplier)
        # Create the new entry in the new recipe dictionary
        new_recipe[ingredient] = f'{new_quantity} {unit}'
    return new_recipe