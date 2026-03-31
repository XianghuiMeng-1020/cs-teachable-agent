def calculate_ingredients(recipes):
    ingredients_dict = {}
    
    for recipe in recipes:
        ingredients = recipe.split()
        for item in ingredients:
            quantity, ingredient = item.split(':')
            quantity = int(quantity)
            if ingredient in ingredients_dict:
                ingredients_dict[ingredient] += quantity
            else:
                ingredients_dict[ingredient] = quantity
    
    return ingredients_dict