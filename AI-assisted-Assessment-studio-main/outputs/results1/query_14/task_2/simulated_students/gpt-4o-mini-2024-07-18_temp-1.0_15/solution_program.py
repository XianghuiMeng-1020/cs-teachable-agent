def get_ingredient_list(recipe_text):
    ingredients = {}
    lines = recipe_text.split('\n')
    for line in lines:
        parts = line.split(maxsplit=2)  # split into at most 3 parts
        if len(parts) == 3:
            quantity = parts[0] + ' ' + parts[1]
            ingredient_name = parts[2].lower()
        elif len(parts) == 2:
            quantity = parts[0]
            ingredient_name = parts[1].lower()
        elif len(parts) == 1:
            quantity = ''
            ingredient_name = parts[0].lower()
        else:
            continue  # in case of empty lines
        ingredients[ingredient_name] = quantity.strip()
    return ingredients