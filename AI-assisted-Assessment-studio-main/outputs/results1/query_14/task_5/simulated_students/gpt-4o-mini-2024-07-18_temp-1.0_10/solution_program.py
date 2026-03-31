def parse_ingredient_list(ingredient_str):
    ingredients = {}
    for item in ingredient_str.split(';'):
        parts = item.split(',')
        name = parts[0].strip()
        quantity = parts[1].strip()
        unit = parts[2].strip()
        ingredients[name] = {'quantity': quantity, 'unit': unit}
    return ingredients