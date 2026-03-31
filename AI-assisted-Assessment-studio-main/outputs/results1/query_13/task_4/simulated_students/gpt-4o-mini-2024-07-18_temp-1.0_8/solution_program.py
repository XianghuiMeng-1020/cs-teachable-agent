def calculate_total_ingredients(ingredient_list):
    total_ingredients = {}
    
    for item in ingredient_list:
        try:
            ingredient, quantity = item.split(':')
            quantity = int(quantity)
            if quantity <= 0:
                continue
            if ingredient in total_ingredients:
                total_ingredients[ingredient] += quantity
            else:
                total_ingredients[ingredient] = quantity
        except (ValueError, TypeError):
            continue
    
    return total_ingredients