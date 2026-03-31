def get_ingredient_list(recipe_text):
    ingredients = recipe_text.split('\n')
    ingredient_dict = {}
    
    for item in ingredients:
        parts = item.split()
        
        if len(parts) == 0:
            continue
        elif len(parts) == 1:
            # Only the ingredient name is present
            ingredient_name = parts[0].lower()
            ingredient_dict[ingredient_name] = ''
        else:
            # At least quantity + ingredient_name or quantity + unit + ingredient_name
            *quantity_unit, ingredient_name = parts
            ingredient_name = ingredient_name.lower()
            ingredient_dict[ingredient_name] = ' '.join(quantity_unit)

    return ingredient_dict

# Example usage
recipe_text = "2 cups flour\n1/2 teaspoon salt\negg"
print(get_ingredient_list(recipe_text))
# Output: {'flour': '2 cups', 'salt': '1/2 teaspoon', 'egg': ''}