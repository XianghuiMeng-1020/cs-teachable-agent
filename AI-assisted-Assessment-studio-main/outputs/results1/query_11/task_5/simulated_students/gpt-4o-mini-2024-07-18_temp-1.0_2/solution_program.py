def ingredient_converter(recipe, conversion_factor):
    adjusted_recipe = []
    for ingredient in recipe:
        quantity_str, unit, *ingredient_name = ingredient.split()
        quantity = float(quantity_str) * conversion_factor
        adjusted_recipe.append(f'{quantity} {unit} {' '.join(ingredient_name)}')
    return adjusted_recipe