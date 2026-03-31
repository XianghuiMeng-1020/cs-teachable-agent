def get_ingredient_list(recipe_text):
    ingredient_dict = {}
    lines = recipe_text.strip().split('\n')
    for line in lines:
        parts = line.strip().split(' ')
        if len(parts) == 0:
            continue
        if len(parts) == 1:
            ingredient_name = parts[0]
            ingredient_dict[ingredient_name.lower()] = ""
        else:
            quantity = parts[0]
            unit = parts[1]
            ingredient_name = ' '.join(parts[2:])
            ingredient_dict[ingredient_name.lower()] = f'{quantity} {unit}'
    return ingredient_dict