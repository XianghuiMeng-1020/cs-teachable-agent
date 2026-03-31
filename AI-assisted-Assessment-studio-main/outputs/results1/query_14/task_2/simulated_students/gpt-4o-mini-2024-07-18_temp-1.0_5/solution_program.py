def get_ingredient_list(recipe_text):
    ingredients = {}
    lines = recipe_text.strip().split('\n')
    for line in lines:
        parts = line.split()  
        if len(parts) == 0:
            continue  
        if len(parts) >= 3:
            quantity = ' '.join(parts[:-2])
            ingredient_name = parts[-1]
        elif len(parts) == 2:
            quantity = parts[0]
            ingredient_name = parts[1]
        else:
            quantity = ''
            ingredient_name = parts[0]
        ingredients[ingredient_name.lower()] = quantity.strip()  
    return ingredients