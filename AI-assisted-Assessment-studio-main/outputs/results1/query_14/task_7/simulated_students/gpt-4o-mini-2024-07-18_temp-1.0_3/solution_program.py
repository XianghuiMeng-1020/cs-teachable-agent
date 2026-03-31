def recipe_calculator(recipe, multiplier):
    result = {}
    for ingredient, quantity in recipe.items():
        # Split the quantity into number and unit
        number, unit = quantity.split(' ', 1)
        # Convert quantity to number and multiply
        new_quantity = round(int(number) * multiplier)
        # Create new ingredient entry
        result[ingredient] = f'{new_quantity} {unit}'
    return result