def calculate_total_ingredients(ingredient_list):
    total_ingredients = {}

    for ingredient in ingredient_list:
        try:
            name, quantity = ingredient.split(':')
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
            if name in total_ingredients:
                total_ingredients[name] += quantity
            else:
                total_ingredients[name] = quantity
        except (ValueError, TypeError, IndexError):
            continue

    return total_ingredients