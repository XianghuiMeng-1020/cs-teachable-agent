def get_ingredient_list(recipe_text):
    ingredients = recipe_text.split('\n')
    ingredient_dict = {}
    
    for ingredient in ingredients:
        parts = ingredient.strip().split(' ')
        if len(parts) >= 3:
            quantity = ' '.join(parts[:2])
            name = ' '.join(parts[2:]).lower()
            ingredient_dict[name] = quantity
        elif len(parts) == 2:
            name = ' '.join(parts[1:]).lower()
            ingredient_dict[name] = parts[0]
        elif len(parts) == 1:
            name = parts[0].lower()
            ingredient_dict[name] = ''
    
    return ingredient_dict