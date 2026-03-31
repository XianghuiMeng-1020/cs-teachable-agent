def ingredient_converter(recipe, conversion_factor):
    adjusted_recipe = []
    for ingredient in recipe:
        quantity, unit, *ingredient_name = ingredient.split()
        new_quantity = float(quantity) * conversion_factor
        adjusted_recipe.append(f'{new_quantity} {unit} {" ".join(ingredient_name)}')
    return adjusted_recipe