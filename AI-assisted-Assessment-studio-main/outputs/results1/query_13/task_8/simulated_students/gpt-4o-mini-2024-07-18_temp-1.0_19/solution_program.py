def calculate_ingredients(recipes):
    ingredient_totals = {}

    for recipe in recipes:
        ingredients = recipe.split()  # Split the recipe into ingredients
        for item in ingredients:
            quantity, ingredient = item.split(':')  # Split quantity and ingredient
            quantity = int(quantity)  # Convert quantity to integer

            if ingredient in ingredient_totals:
                ingredient_totals[ingredient] += quantity  # Add to existing total
            else:
                ingredient_totals[ingredient] = quantity  # Initialize with the quantity

    return ingredient_totals