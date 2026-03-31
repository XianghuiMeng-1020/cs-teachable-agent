def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for item in recipe:
        quantity_str, unit, ingredient = item.split(' ', 2)
        quantity = float(quantity_str) * conversion_factor
        converted_recipe.append(f'{quantity} {unit} {ingredient}')
    return converted_recipe