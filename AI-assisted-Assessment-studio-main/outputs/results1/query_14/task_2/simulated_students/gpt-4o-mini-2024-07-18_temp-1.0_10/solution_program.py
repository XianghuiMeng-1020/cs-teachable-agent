def get_ingredient_list(recipe_text):
    ingredient_dict = {}
    lines = recipe_text.strip().split('\n')
    for line in lines:
        parts = line.split(maxsplit=2)
        if len(parts) == 3:
            quantity_and_unit = f'{parts[0]} {parts[1]}'
            ingredient_name = parts[2]
        elif len(parts) == 2:
            quantity_and_unit = parts[0]
            ingredient_name = parts[1]
        else:
            quantity_and_unit = ''
            ingredient_name = parts[0]
        ingredient_dict[ingredient_name.lower()] = quantity_and_unit
    return ingredient_dict