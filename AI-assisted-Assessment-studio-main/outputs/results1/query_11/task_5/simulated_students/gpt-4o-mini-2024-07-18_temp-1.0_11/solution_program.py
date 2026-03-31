def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for item in recipe:
        quantity, unit, *ingredient_name = item.split()
        new_quantity = float(quantity) * conversion_factor
        new_item = f'{new_quantity} {unit} {' '.join(ingredient_name)}'
        converted_recipe.append(new_item)
    return converted_recipe