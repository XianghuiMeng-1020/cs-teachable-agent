def get_ingredient_list(recipe_text):
    lines = recipe_text.split('\n')
    ingredients_dict = {}
    for line in lines:
        parts = line.split()  
        if len(parts) == 1:  
            ingredient_name = parts[0].lower()
            ingredient_detail = ""
        else:
            ingredient_name = parts[2].lower() if len(parts) > 2 else parts[0].lower()
            ingredient_detail = " ".join(parts[:2]) if len(parts) > 2 else ""
        ingredients_dict[ingredient_name] = ingredient_detail
    return ingredients_dict
