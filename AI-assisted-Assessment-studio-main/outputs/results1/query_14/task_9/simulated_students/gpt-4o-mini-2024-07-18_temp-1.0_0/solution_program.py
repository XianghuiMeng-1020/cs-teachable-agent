def parse_ingredient_list(ingredient_string):
    ingredients = ingredient_string.split(';')
    ingredient_dict = {}
    for ingredient in ingredients:
        name, quantity = ingredient.split(':')
        ingredient_dict[name] = quantity
    return ingredient_dict