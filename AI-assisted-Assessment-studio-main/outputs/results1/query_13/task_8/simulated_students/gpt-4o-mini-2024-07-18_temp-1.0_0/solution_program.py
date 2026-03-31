def calculate_ingredients(recipes):
    ingredient_totals = {}
    for recipe in recipes:
        for item in recipe.split():
            quantity, ingredient = item.split(':')
            quantity = int(quantity)
            if ingredient in ingredient_totals:
                ingredient_totals[ingredient] += quantity
            else:
                ingredient_totals[ingredient] = quantity
    return ingredient_totals