def get_ingredient_list(recipe_text):
    ingredients = recipe_text.strip().split('\n')
    ingredient_dict = {}

    for ingredient in ingredients:
        parts = ingredient.split(maxsplit=2)
        if len(parts) == 3:
            quantity_unit = ' '.join(parts[:2])
            name = parts[2]
        elif len(parts) == 2:
            quantity_unit = parts[0]
            name = parts[1]
        else:
            quantity_unit = ''
            name = parts[0]

        ingredient_dict[name.lower()] = quantity_unit

    return ingredient_dict