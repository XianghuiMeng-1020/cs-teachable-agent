def vegetable_counter(order):
    vegetable_totals = {}

    for dish in order:
        dish_content = dish.split(': ')[1]  # Get the part after the ':'
        vegetables = dish_content.split(', ')

        for vegetable in vegetables:
            name, quantity = vegetable.split('=')
            quantity = int(quantity)
            if name in vegetable_totals:
                vegetable_totals[name] += quantity
            else:
                vegetable_totals[name] = quantity

    sorted_vegetables = sorted(vegetable_totals.items())
    result = [f'{name}={quantity}' for name, quantity in sorted_vegetables]
    return str(result)