def get_ingredient_list(recipe_text):
    ingredients = recipe_text.strip().split('\n')
    ingredient_dict = {}

    for item in ingredients:
        parts = item.split(maxsplit=2)
        if len(parts) == 3:
            quantity = f'{parts[0]} {parts[1]}'
            ingredient_name = parts[2]
        elif len(parts) == 2:
            quantity = parts[0]
            ingredient_name = parts[1]
        else:
            quantity = ''
            ingredient_name = parts[0]

        # Normalize the ingredient name to lowercase for case-insensitivity
        ingredient_dict[ingredient_name.lower()] = quantity

    return ingredient_dict