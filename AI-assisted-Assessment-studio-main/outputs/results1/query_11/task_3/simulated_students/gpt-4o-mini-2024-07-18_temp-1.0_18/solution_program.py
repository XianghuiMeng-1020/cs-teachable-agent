def vegetable_counter(order):
    vegetable_totals = {}

    for dish in order:
        parts = dish.split(':')
        ingredients = parts[1].split(', ')

        for ingredient in ingredients:
            veg, quantity = ingredient.split('=')
            quantity = int(quantity)
            if veg in vegetable_totals:
                vegetable_totals[veg] += quantity
            else:
                vegetable_totals[veg] = quantity

    sorted_vegetables = sorted(vegetable_totals.items())
    result = [f'{veg}={qty}' for veg, qty in sorted_vegetables]
    return str(result)