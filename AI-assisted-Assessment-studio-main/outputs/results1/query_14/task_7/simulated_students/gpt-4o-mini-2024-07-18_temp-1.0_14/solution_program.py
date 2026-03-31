def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split the quantity to separate the numeric part from the unit
        num_part, unit = quantity.split(' ', 1)
        # Convert the numeric part to an integer and multiply
        new_quantity = round(int(num_part) * multiplier)
        # Build the new quantity string
        new_recipe[ingredient] = f'{new_quantity} {unit}'
    return new_recipe