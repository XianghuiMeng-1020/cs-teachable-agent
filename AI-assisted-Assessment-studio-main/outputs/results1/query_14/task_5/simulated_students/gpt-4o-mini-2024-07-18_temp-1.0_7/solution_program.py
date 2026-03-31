def parse_ingredient_list(ingredient_str):
    ingredients = ingredient_str.split(';')
    result = {}
    for ingredient in ingredients:
        parts = ingredient.split(',')
        name = parts[0].strip()
        quantity = parts[1].strip()
        unit = parts[2].strip()
        result[name] = {'quantity': quantity, 'unit': unit}
    return result