def get_ingredient_list(recipe_text):
    ingredients = recipe_text.strip().split('\n')
    ingredient_dict = {}
    for ingredient in ingredients:
        parts = ingredient.split(None, 2)  # Split by whitespace, max 2 splits
        if len(parts) == 3:
            quantity = parts[0] + ' ' + parts[1]
            name = parts[2]
        elif len(parts) == 2:
            quantity = parts[0]
            name = parts[1]
        elif len(parts) == 1:
            quantity = ''
            name = parts[0]
        else:
            continue
        ingredient_dict[name.lower()] = quantity
    return ingredient_dict