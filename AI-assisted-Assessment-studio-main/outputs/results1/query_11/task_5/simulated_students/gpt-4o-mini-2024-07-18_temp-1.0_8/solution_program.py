def ingredient_converter(recipe, conversion_factor):
    adjusted_recipe = []
    for ingredient in recipe:
        # Split the ingredient string into parts: quantity, unit, and name
        parts = ingredient.split(' ', 2)
        quantity = float(parts[0]) * conversion_factor
        adjusted_ingredient = f'{quantity} {parts[1]} {parts[2]}'
        adjusted_recipe.append(adjusted_ingredient)
    return adjusted_recipe