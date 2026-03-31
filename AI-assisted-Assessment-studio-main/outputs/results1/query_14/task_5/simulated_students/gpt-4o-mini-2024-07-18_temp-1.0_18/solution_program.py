def parse_ingredient_list(ingredient_str):
    ingredients = ingredient_str.split(';')
    ingredient_dict = {}
    
    for ingredient in ingredients:
        name, quantity, unit = map(str.strip, ingredient.split(','))
        ingredient_dict[name] = {'quantity': quantity, 'unit': unit}
    
    return ingredient_dict