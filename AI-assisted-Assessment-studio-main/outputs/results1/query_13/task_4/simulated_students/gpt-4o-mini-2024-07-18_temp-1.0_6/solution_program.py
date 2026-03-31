def calculate_total_ingredients(ingredient_list):
    total_ingredients = {}

    for entry in ingredient_list:
        try:
            ingredient, quantity_str = entry.split(':')
            if not ingredient or not quantity_str:
                continue
            quantity = int(quantity_str)
            if quantity <= 0:
                continue
            if ingredient in total_ingredients:
                total_ingredients[ingredient] += quantity
            else:
                total_ingredients[ingredient] = quantity
        except (ValueError, TypeError):
            continue

    return total_ingredients