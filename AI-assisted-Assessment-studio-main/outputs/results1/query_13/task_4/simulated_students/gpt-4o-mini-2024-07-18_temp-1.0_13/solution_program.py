def calculate_total_ingredients(ingredient_list):
    totals = {}
    for item in ingredient_list:
        try:
            ingredient, quantity = item.split(':')
            quantity = int(quantity)
            if quantity <= 0:
                continue
            if ingredient in totals:
                totals[ingredient] += quantity
            else:
                totals[ingredient] = quantity
        except (ValueError, TypeError):
            continue
    return totals