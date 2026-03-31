def get_ingredient_list(recipe_text):
    ingredients = {}
    lines = recipe_text.strip().split('\n')
    for line in lines:
        parts = line.split(maxsplit=2)
        if len(parts) == 3:
            quantity = parts[0] + ' ' + parts[1]
            ingredient_name = parts[2]
        elif len(parts) == 2:
            quantity = parts[0]
            ingredient_name = parts[1]
        elif len(parts) == 1:
            quantity = ''
            ingredient_name = parts[0]
        else:
            continue
        ingredient_name_lower = ingredient_name.lower()
        ingredients[ingredient_name_lower] = quantity.strip() if quantity else ''
    return ingredients