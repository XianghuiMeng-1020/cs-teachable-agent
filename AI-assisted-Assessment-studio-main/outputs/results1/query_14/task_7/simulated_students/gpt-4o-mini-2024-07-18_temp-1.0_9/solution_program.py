def recipe_calculator(recipe, multiplier):
    result = {}
    for ingredient, quantity in recipe.items():
        number, unit = quantity.split(' ', 1)
        number = int(number) * multiplier
        result[ingredient] = f'{round(number)} {unit}'
    return result