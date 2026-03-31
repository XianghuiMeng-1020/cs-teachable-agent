def vegetable_counter(order):
    vegetable_totals = {}
    for dish in order:
        dish_parts = dish.split(':')
        vegetables = dish_parts[1].split(',')
        for vegetable in vegetables:
            name, quantity = vegetable.strip().split('=')
            quantity = int(quantity)
            if name in vegetable_totals:
                vegetable_totals[name] += quantity
            else:
                vegetable_totals[name] = quantity
    sorted_vegetables = sorted(vegetable_totals.items())
    result = [f'{name}={quantity}' for name, quantity in sorted_vegetables]
    return str(result)