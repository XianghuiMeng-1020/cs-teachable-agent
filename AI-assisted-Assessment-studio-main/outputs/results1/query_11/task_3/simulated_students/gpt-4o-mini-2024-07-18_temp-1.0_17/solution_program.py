def vegetable_counter(order):
    vegetable_totals = {}

    for dish in order:
        _, ingredients = dish.split(': ')
        for ingredient in ingredients.split(', '):
            vegetable, quantity = ingredient.split('=')
            quantity = int(quantity)
            if vegetable in vegetable_totals:
                vegetable_totals[vegetable] += quantity
            else:
                vegetable_totals[vegetable] = quantity

    sorted_vegetables = sorted(vegetable_totals.items())
    result = [f'{veg}={qty}' for veg, qty in sorted_vegetables]

    return str(result)