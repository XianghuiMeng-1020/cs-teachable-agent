def get_ingredient_list(recipe_text):
    ingredients = recipe_text.split('\n')
    ingredient_dict = {}
    for ingredient in ingredients:
        parts = ingredient.split()  
        if len(parts) >= 3:
            quantity_and_unit = ' '.join(parts[:2])
            ingredient_name = ' '.join(parts[2:])
        elif len(parts) == 2:
            quantity_and_unit = parts[0]
            ingredient_name = parts[1]
        elif len(parts) == 1:
            quantity_and_unit = ''
            ingredient_name = parts[0]
        else:
            continue
        ingredient_dict[ingredient_name.lower()] = quantity_and_unit
    return ingredient_dict