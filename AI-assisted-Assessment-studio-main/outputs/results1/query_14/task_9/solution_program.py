def parse_ingredient_list(ingredient_string):
    ingredients = {}
    if ingredient_string:
        parts = ingredient_string.split(';')
        for part in parts:
            if ':' in part:
                ingredient, quantity = part.split(':')
                ingredients[ingredient.strip()] = quantity.strip()
    return ingredients