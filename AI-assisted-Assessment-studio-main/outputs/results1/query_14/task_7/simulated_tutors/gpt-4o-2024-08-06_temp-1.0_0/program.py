def recipe_calculator(recipe, multiplier):
    updated_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split quantity from unit
        parts = quantity.split(" ", 1)
        numerical_quantity, unit = parts[0], parts[1]
        # Multiply and round
        new_quantity = round(int(numerical_quantity) * multiplier)
        # Formulate new entry
        updated_recipe[ingredient] = f"{new_quantity} {unit}"
    return updated_recipe
