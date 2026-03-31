def calculate_ingredients(recipes):
    ingredients_count = {}
    for recipe in recipes:
        ingredients = recipe.split()
        for ingredient in ingredients:
            quantity, name = ingredient.split(':')
            quantity = int(quantity)
            if name in ingredients_count:
                ingredients_count[name] += quantity
            else:
                ingredients_count[name] = quantity
    return ingredients_count