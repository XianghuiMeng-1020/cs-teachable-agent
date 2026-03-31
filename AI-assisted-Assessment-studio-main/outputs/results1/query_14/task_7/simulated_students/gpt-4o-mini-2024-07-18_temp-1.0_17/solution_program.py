def recipe_calculator(recipe, multiplier):
    result = {}
    for ingredient, quantity in recipe.items():
        # Split the quantity into number and unit
        quantity_number = int(quantity.split(' ')[0])
        unit = ' '.join(quantity.split(' ')[1:])
        # Calculate new quantity
        new_quantity = round(quantity_number * multiplier)
        # Create new entry in result dictionary
        result[ingredient] = f'{new_quantity} {unit}'
    return result