def vegetable_counter(order):
    vegetable_count = {}

    for dish in order:
        _, veg_str = dish.split(':')
        vegetables = veg_str.split(',')
        for vegetable in vegetables:
            name, quantity = vegetable.split('=')
            name = name.strip()
            quantity = int(quantity.strip())
            if name in vegetable_count:
                vegetable_count[name] += quantity
            else:
                vegetable_count[name] = quantity

    sorted_vegetables = sorted(vegetable_count.items())
    result = [f'{name}={qty}' for name, qty in sorted_vegetables]
    return str(result)