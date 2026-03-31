def parse_ingredient_list(ingredient_str):
    ingredient_dict = {}
    ingredients = ingredient_str.split(';')
    for ingredient in ingredients:
        parts = ingredient.split(',')
        if len(parts) == 3:
            name = parts[0].strip().lower()
            quantity = parts[1].strip()
            unit = parts[2].strip().lower()
            ingredient_dict[name] = {'quantity': quantity, 'unit': unit}
    return ingredient_dict