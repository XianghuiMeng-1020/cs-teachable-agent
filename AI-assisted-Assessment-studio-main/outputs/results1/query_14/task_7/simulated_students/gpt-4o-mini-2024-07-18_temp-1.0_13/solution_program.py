def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        number_part, unit_part = quantity.split(' ', 1)
        new_quantity = round(int(number_part) * multiplier)
        new_recipe[ingredient] = f'{new_quantity} {unit_part}'
    return new_recipe