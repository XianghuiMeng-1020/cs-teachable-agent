def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for item in recipe:
        parts = item.split(' ', 2)
        quantity = float(parts[0]) * conversion_factor
        converted_item = f'{quantity} {parts[1]} {parts[2]}'
        converted_recipe.append(converted_item)
    return converted_recipe