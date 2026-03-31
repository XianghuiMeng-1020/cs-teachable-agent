def calculate_total_ingredients(ingredient_list):
    total_ingredients = {}
    for entry in ingredient_list:
        try:
            ingredient, quantity_str = entry.split(':')
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
            if ingredient in total_ingredients:
                total_ingredients[ingredient] += quantity
            else:
                total_ingredients[ingredient] = quantity
        except (ValueError, IndexError):
            continue
    return total_ingredients