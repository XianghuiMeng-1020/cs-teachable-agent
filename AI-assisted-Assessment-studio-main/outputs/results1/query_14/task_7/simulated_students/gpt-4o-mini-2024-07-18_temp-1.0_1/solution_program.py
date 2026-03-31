def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split quantity from the unit
        quantity_num, unit = quantity.split(' ', 1)
        # Convert quantity to int and multiply by the multiplier
        new_quantity = round(int(quantity_num) * multiplier)
        # Update the new recipe dictionary
        new_recipe[ingredient] = f'{new_quantity} {unit}'
    return new_recipe