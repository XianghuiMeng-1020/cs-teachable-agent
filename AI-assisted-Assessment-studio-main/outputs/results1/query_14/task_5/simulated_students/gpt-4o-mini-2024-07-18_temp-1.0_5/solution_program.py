def parse_ingredient_list(ingredient_str):
    ingredient_list = ingredient_str.split(';')
    ingredients_dict = {}
    
    for ingredient in ingredient_list:
        parts = ingredient.split(',')
        name = parts[0].strip()
        quantity = parts[1].strip()
        unit = parts[2].strip()
        ingredients_dict[name] = {'quantity': quantity, 'unit': unit}
    
    return ingredients_dict