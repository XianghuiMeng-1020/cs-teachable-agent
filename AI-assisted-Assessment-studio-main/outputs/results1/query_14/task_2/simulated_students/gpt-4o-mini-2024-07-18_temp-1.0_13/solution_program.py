def get_ingredient_list(recipe_text):
    ingredients = recipe_text.strip().split('\n')
    ingredient_dict = {}
    for ingredient in ingredients:
        parts = ingredient.strip().split(' ')
        if len(parts) >= 3:
            quantity = ' '.join(parts[:2])
            name = ' '.join(parts[2:])
        elif len(parts) == 2:
            quantity = parts[0]
            name = parts[1]
        else:
            quantity = ''
            name = parts[0]
        ingredient_dict[name.lower()] = quantity.strip()
    return ingredient_dict