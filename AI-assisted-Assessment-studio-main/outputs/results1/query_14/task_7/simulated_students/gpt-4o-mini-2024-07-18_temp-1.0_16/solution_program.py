def recipe_calculator(recipe, multiplier):
    result = {}
    for ingredient, quantity in recipe.items():
        num, unit = quantity.split(' ', 1)
        num = int(num)
        new_quantity = round(num * multiplier)
        result[ingredient] = f'{new_quantity} {unit}'
    return result