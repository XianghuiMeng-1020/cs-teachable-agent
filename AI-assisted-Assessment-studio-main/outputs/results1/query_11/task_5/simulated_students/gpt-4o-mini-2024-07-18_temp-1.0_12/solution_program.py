def ingredient_converter(recipe, conversion_factor):
    adjusted_recipe = []
    for item in recipe:
        quantity, unit, *ingredient_name = item.split()
        adjusted_quantity = float(quantity) * conversion_factor
        adjusted_item = f'{adjusted_quantity} {unit} {' '.join(ingredient_name)}'
        adjusted_recipe.append(adjusted_item)
    return adjusted_recipe