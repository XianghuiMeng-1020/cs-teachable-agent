def calculate_ingredients(recipes):
    ingredient_totals = {}
    
    for recipe in recipes:
        ingredients = recipe.split()
        for ingredient in ingredients:
            quantity, name = ingredient.split(':')
            quantity = int(quantity)
            if name in ingredient_totals:
                ingredient_totals[name] += quantity
            else:
                ingredient_totals[name] = quantity
    
    return ingredient_totals