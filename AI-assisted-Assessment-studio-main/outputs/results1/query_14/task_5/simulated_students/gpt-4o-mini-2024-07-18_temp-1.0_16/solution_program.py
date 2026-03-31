def parse_ingredient_list(ingredient_str):
    ingredient_dict = {}
    ingredients = ingredient_str.split(';')
    for item in ingredients:
        item = item.strip()
        if item:
            name, quantity, unit = map(str.strip, item.split(','))
            ingredient_dict[name] = {'quantity': quantity, 'unit': unit}
    return ingredient_dict