def calculate_ingredients(recipes):
    ingredient_dict = {}
    for recipe in recipes:
        ingredients = recipe.split()
        for item in ingredients:
            quantity, ingredient = item.split(':')
            quantity = int(quantity)
            if ingredient in ingredient_dict:
                ingredient_dict[ingredient] += quantity
            else:
                ingredient_dict[ingredient] = quantity
    return ingredient_dict