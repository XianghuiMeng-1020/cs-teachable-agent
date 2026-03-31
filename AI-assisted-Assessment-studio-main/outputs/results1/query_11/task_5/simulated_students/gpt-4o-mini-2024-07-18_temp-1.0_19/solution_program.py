def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for ingredient in recipe:
        parts = ingredient.split(' ', 2)
        quantity = float(parts[0]) * conversion_factor
        converted_recipe.append(f'{quantity} {parts[1]} {parts[2]}')
    return converted_recipe