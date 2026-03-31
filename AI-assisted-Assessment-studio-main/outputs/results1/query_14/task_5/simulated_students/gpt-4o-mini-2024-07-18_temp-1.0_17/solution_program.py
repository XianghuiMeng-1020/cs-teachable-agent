def parse_ingredient_list(ingredient_str):
    ingredient_dict = {}
    ingredients = ingredient_str.split(';')
    for ingredient in ingredients:
        parts = [part.strip() for part in ingredient.split(',')]
        name = parts[0]
        quantity = parts[1]
        unit = parts[2]
        ingredient_dict[name] = {'quantity': quantity, 'unit': unit}
    return ingredient_dict