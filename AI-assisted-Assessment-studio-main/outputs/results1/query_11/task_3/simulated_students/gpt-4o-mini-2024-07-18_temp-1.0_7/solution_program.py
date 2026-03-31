def vegetable_counter(order):
    vegetable_count = {}

    for dish in order:
        _, ingredients = dish.split(': ')
        vegetable_pairs = ingredients.split(', ')
        for pair in vegetable_pairs:
            vegetable, quantity = pair.split('=')
            quantity = int(quantity)
            if vegetable in vegetable_count:
                vegetable_count[vegetable] += quantity
            else:
                vegetable_count[vegetable] = quantity

    sorted_vegetables = sorted(vegetable_count.items())
    result = [f'{veg}={qty}' for veg, qty in sorted_vegetables]
    return str(result)