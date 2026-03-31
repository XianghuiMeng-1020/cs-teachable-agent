def recipe_calculator(recipe, multiplier):
    result = {}
    for ingredient, quantity in recipe.items():
        number_of_units = int(quantity.split()[0])
        unit = ' '.join(quantity.split()[1:])
        new_quantity = round(number_of_units * multiplier)
        result[ingredient] = f'{new_quantity} {unit}'
    return result