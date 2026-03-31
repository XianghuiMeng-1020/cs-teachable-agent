def recipe_calculator(recipe, multiplier):
    new_recipe = {}
    for ingredient, quantity in recipe.items():
        # Split quantity into number and unit
        number_str, unit = quantity.split(' ', 1)
        number = int(number_str) * multiplier
        # Round to nearest integer
        rounded_number = round(number)
        # Create a new entry in the new recipe dictionary
        new_recipe[ingredient] = f'{rounded_number} {unit}'
    return new_recipe