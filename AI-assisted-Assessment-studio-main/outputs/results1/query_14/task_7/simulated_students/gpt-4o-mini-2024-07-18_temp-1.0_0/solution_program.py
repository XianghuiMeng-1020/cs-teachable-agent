def recipe_calculator(recipe, multiplier):
    result = {}
    for ingredient, quantity in recipe.items():
        # Split the quantity string and convert the numeric part to integer
        num = int(quantity.split()[0])
        # Multiply the quantity by the multiplier
        new_quantity = round(num * multiplier)
        # Keep the unit part the same
        unit = ' '.join(quantity.split()[1:])
        # Create the new entry in the result dictionary
        result[ingredient] = f'{new_quantity} {unit}'
    return result