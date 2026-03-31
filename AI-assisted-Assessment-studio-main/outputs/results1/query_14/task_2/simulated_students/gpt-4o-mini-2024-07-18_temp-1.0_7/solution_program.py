def get_ingredient_list(recipe_text):
    ingredient_dict = {}
    ingredients = recipe_text.split('\n')
    for ingredient in ingredients:
        parts = ingredient.strip().split(' ')
        if len(parts) >= 3:
            quantity = ' '.join(parts[:-2])
            unit = parts[-2]
            name = parts[-1]
            ingredient_dict[name.lower()] = f'{quantity} {unit}'
        elif len(parts) == 2:
            unit = parts[-2]
            name = parts[-1]
            ingredient_dict[name.lower()] = f'{unit}'
        elif len(parts) == 1:
            name = parts[0]
            ingredient_dict[name.lower()] = ''
    return ingredient_dict