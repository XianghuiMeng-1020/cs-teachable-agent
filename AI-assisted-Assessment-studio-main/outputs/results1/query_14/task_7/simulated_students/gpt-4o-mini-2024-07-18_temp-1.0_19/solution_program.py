def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split the quantity from the unit
        quantity_number, unit = quantity.split(' ', 1)
        # Convert quantity to integer
        quantity_number = int(quantity_number)
        # Calculate new quantity and round it
        new_quantity = round(quantity_number * multiplier)
        # Recreate the quantity string
        new_recipe[ingredient] = f'{new_quantity} {unit}'
    return new_recipe