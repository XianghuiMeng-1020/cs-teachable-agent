def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split the quantity and unit
        quantity_value, unit = quantity.split(' ', 1)
        quantity_value = int(quantity_value)  # Convert quantity to integer
        # Calculate new quantity and round it
        new_quantity = round(quantity_value * multiplier)
        # Create new entry in the new recipe dictionary
        new_recipe[ingredient] = f'{new_quantity} {unit}'
    return new_recipe