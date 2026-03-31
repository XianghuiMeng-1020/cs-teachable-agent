def get_ingredient_list(recipe_text):
    ingredients_dict = {}
    lines = recipe_text.split('\n')
    for line in lines:
        parts = line.split(maxsplit=2)
        if len(parts) == 3:
            quantity_unit = f'{parts[0]} {parts[1]}'
            ingredient_name = parts[2]
        elif len(parts) == 2:
            quantity_unit = parts[0]
            ingredient_name = parts[1]
        else:
            quantity_unit = ''
            ingredient_name = parts[0]

        ingredients_dict[ingredient_name.lower()] = quantity_unit
    return ingredients_dict