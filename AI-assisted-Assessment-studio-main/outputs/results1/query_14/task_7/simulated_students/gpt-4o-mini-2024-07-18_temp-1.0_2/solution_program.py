def recipe_calculator(recipe, multiplier):
    result = {}
    for ingredient, quantity in recipe.items():
        number, unit = quantity.split(' ', 1)
        number = int(number) * multiplier
        if number % 1:
            number = round(number)
        result[ingredient] = f'{number} {unit}'
    return result