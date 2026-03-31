def calculate_ingredients(recipes):
    ingredients = {}
    for recipe in recipes:
        for item in recipe.split():
            quantity, ingredient = item.split(':')
            quantity = int(quantity)
            if ingredient in ingredients:
                ingredients[ingredient] += quantity
            else:
                ingredients[ingredient] = quantity
    return ingredients