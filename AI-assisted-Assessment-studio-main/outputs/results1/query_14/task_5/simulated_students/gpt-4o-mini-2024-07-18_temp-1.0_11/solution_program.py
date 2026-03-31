def parse_ingredient_list(ingredient_str):
    ingredients = ingredient_str.split(';')
    ingredient_dict = {}
    for ingredient in ingredients:
        # Strip any leading/trailing whitespace and split by comma
        parts = ingredient.strip().split(',')
        name = parts[0].strip()
        quantity = parts[1].strip()
        unit = parts[2].strip()
        ingredient_dict[name] = {'quantity': quantity, 'unit': unit}
    return ingredient_dict