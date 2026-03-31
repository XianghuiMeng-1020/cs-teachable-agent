def get_ingredient_list(recipe_text):
    ingredient_dict = {}
    lines = recipe_text.strip().split('\n')
    for line in lines:
        parts = line.split(maxsplit=2)
        if len(parts) == 3:
            quantity = parts[0] + ' ' + parts[1]
            ingredient_name = parts[2]
        elif len(parts) == 2:
            quantity = parts[0]
            ingredient_name = parts[1]
        else:
            quantity = ''
            ingredient_name = parts[0]
        ingredient_dict[ingredient_name.lower()] = quantity.strip()
    return ingredient_dict