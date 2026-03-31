def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for item in recipe:
        quantity, unit, *ingredient = item.split()
        quantity = float(quantity) * conversion_factor
        ingredient_name = ' '.join(ingredient)
        converted_recipe.append(f'{quantity} {unit} {ingredient_name}')
    return converted_recipe