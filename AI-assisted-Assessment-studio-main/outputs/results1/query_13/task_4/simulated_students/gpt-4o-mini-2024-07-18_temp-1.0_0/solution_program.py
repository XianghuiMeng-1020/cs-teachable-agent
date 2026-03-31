def calculate_total_ingredients(ingredient_list):
    total_ingredients = {}
    for entry in ingredient_list:
        try:
            ingredient, quantity = entry.split(':')
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError('Quantity must be positive')
        except (ValueError, IndexError):
            continue
        if ingredient in total_ingredients:
            total_ingredients[ingredient] += quantity
        else:
            total_ingredients[ingredient] = quantity
    return total_ingredients