def calculate_ingredients(recipes):
    ingredients_totals = {}
    for recipe in recipes:
        parts = recipe.split()
        for part in parts:
            try:
                quantity, ingredient = part.split(':')
                quantity = int(quantity)
                if ingredient in ingredients_totals:
                    ingredients_totals[ingredient] += quantity
                else:
                    ingredients_totals[ingredient] = quantity
            except ValueError:
                pass
    return ingredients_totals