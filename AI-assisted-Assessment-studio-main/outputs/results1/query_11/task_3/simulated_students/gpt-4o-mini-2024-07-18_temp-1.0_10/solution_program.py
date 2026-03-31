def vegetable_counter(order):
    vegetable_totals = {}

    for dish in order:
        dish_name, ingredients = dish.split(':')
        ingredient_list = ingredients.split(', ')
        for item in ingredient_list:
            vegetable, quantity = item.split('=')
            quantity = int(quantity)
            if vegetable in vegetable_totals:
                vegetable_totals[vegetable] += quantity
            else:
                vegetable_totals[vegetable] = quantity

    sorted_vegetables = sorted(vegetable_totals.items())
    result = [f'{veg}={qty}' for veg, qty in sorted_vegetables]

    return str(result)