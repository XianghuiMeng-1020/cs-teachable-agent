def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split the quantity to convert to an integer
        num_quantity = int(quantity.split()[0])
        # Multiply and round the quantity
        new_quantity = round(num_quantity * multiplier)
        # Create new recipe entry with updated quantity
        new_recipe[ingredient] = f'{new_quantity} {" ".join(quantity.split()[1:])}'
    return new_recipe