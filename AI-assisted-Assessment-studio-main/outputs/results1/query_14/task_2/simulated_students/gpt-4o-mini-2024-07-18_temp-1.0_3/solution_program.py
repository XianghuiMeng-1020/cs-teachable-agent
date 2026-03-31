def get_ingredient_list(recipe_text):
    ingredients = recipe_text.strip().split('\n')
    ingredient_dict = {}
    
    for ingredient in ingredients:
        parts = ingredient.split()  # Split the line into parts
        if len(parts) >= 3:
            quantity = ' '.join(parts[:2])  # Join the first two parts as quantity and unit
            name = ' '.join(parts[2:])  # Join the rest as ingredient name
        elif len(parts) == 2:
            quantity = parts[0]  # Only quantity is present
            name = parts[1]
        else:
            quantity = ''  # No quantity or unit
            name = parts[0]  # Only ingredient name
        
        ingredient_dict[name.lower()] = quantity
    
    return ingredient_dict