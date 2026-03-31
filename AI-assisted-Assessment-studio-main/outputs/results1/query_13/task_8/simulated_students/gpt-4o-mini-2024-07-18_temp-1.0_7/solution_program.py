def calculate_ingredients(recipes):
    ingredient_dict = {}
    
    for recipe in recipes:
        ingredients = recipe.split()
        
        for ingredient in ingredients:
            quantity, name = ingredient.split(':')
            quantity = int(quantity)
            
            if name in ingredient_dict:
                ingredient_dict[name] += quantity
            else:
                ingredient_dict[name] = quantity
    
    return ingredient_dict