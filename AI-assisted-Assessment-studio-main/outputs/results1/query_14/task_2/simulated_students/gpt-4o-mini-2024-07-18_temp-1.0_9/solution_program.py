def get_ingredient_list(recipe_text):
    ingredients = recipe_text.strip().split('\n')
    ingredient_dict = {}
    
    for ingredient in ingredients:
        parts = ingredient.split()  
        if len(parts) == 0:
            continue  
        if len(parts) == 1:
            ingredient_name = parts[0]
            quantity_unit = ""
        else:
            quantity_unit = " ".join(parts[:-1])
            ingredient_name = parts[-1]
        
        normalized_name = ingredient_name.lower()
        ingredient_dict[normalized_name] = quantity_unit.strip()
    
    return ingredient_dict