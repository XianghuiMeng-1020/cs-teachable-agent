def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for item in recipe:
        quantity, unit, *ingredient = item.split()
        new_quantity = float(quantity) * conversion_factor
        converted_item = f'{new_quantity} {unit} {' '.join(ingredient)}'
        converted_recipe.append(converted_item)
    return converted_recipe