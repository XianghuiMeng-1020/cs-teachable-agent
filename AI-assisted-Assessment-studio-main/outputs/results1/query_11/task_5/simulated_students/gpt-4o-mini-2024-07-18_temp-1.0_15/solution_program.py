def ingredient_converter(recipe, conversion_factor):
    adjusted_recipe = []
    for item in recipe:
        # Split the item into quantity, unit, and ingredient name
        parts = item.split(' ', 2)
        quantity = float(parts[0]) * conversion_factor
        unit = parts[1]
        ingredient_name = parts[2]
        adjusted_recipe.append(f'{quantity} {unit} {ingredient_name}')
    return adjusted_recipe