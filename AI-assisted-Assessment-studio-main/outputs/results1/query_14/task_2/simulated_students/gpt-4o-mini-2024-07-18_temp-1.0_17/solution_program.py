def get_ingredient_list(recipe_text):
    ingredients = recipe_text.strip().split('\n')
    ingredient_dict = {}
    for ingredient in ingredients:
        parts = ingredient.split(maxsplit=2)
        if len(parts) == 3:
            quantity_unit = f'{parts[0]} {parts[1]}'
            ingredient_name = parts[2]
        elif len(parts) == 2:
            quantity_unit = parts[0]
            ingredient_name = parts[1]
        else:
            quantity_unit = ''
            ingredient_name = parts[0]
        ingredient_dict[ingredient_name.lower()] = quantity_unit
    return ingredient_dict