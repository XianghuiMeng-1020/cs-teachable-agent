def ingredient_converter(recipe, conversion_factor):
    converted_recipe = []
    for item in recipe:
        # Split the string into a quantity part and the rest (unit and name)
        parts = item.split(' ', 1)
        quantity = float(parts[0])
        rest = parts[1]
        
        # Calculate the new quantity
        new_quantity = quantity * conversion_factor
        
        # Format the new string with the converted quantity
        new_item = f"{new_quantity} {rest}"
        converted_recipe.append(new_item)
    return converted_recipe