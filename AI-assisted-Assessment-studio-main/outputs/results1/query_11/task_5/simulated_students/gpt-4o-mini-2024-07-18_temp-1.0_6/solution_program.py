def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for ingredient in recipe:
        quantity, unit, *ingredient_name = ingredient.split()
        new_quantity = float(quantity) * conversion_factor
        new_ingredient = f'{new_quantity} {unit} {' '.join(ingredient_name)}'
        converted_recipe.append(new_ingredient)
    return converted_recipe