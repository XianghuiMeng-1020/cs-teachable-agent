def ingredient_converter(recipe, conversion_factor):
    new_recipe = []
    for item in recipe:
        quantity, unit, ingredient_name = item.split(' ', 2)
        adjusted_quantity = float(quantity) * conversion_factor
        new_item = f'{adjusted_quantity} {unit} {ingredient_name}'
        new_recipe.append(new_item)
    return new_recipe