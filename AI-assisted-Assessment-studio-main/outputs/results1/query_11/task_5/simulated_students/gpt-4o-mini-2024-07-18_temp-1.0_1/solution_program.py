def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for ingredient in recipe:
        qty, unit, *name = ingredient.split()
        new_qty = float(qty) * conversion_factor
        new_ingredient = f'{new_qty} {unit} {" ".join(name)}'
        converted_recipe.append(new_ingredient)
    return converted_recipe