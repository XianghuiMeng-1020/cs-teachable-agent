def parse_ingredient_list(ingredient_str):
    ingredients = ingredient_str.split(';')
    ingredient_dict = {}
    
    for ingredient in ingredients:
        parts = [part.strip() for part in ingredient.split(',')]
        if len(parts) == 3:
            name, quantity, unit = parts
            ingredient_dict[name] = {'quantity': quantity, 'unit': unit}
    
    return ingredient_dict