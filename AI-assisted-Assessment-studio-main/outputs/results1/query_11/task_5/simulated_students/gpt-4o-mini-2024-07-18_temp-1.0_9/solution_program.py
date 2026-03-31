def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for ingredient in recipe:
        # Split the ingredient string into parts
        parts = ingredient.split(' ', 2)
        quantity = float(parts[0]) * conversion_factor
        unit = parts[1]
        ingredient_name = parts[2] if len(parts) > 2 else ''
        # Create the new ingredient string and append to the list
        converted_ingredient = f'{quantity} {unit} {ingredient_name}'.strip()
        converted_recipe.append(converted_ingredient)
    return converted_recipe