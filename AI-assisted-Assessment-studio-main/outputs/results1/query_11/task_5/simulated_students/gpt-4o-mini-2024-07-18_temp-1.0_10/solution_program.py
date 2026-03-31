def ingredient_converter(recipe, conversion_factor):
    adjusted_recipe = []
    for ingredient in recipe:
        quantity, unit, *ingredient_name = ingredient.split()
        adjusted_quantity = float(quantity) * conversion_factor
        adjusted_ingredient = f'{adjusted_quantity} {unit} {' '.join(ingredient_name)}'
        adjusted_recipe.append(adjusted_ingredient)
    return adjusted_recipe