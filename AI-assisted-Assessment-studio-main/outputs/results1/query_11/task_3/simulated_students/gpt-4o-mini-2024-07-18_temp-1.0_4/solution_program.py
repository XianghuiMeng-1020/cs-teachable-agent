def vegetable_counter(order):
    vegetable_counts = {}
    for dish in order:
        components = dish.split(':')
        vegetables = components[1].split(',')
        for vegetable in vegetables:
            veg_name, quantity = vegetable.split('=')
            quantity = int(quantity.strip())
            veg_name = veg_name.strip()
            if veg_name in vegetable_counts:
                vegetable_counts[veg_name] += quantity
            else:
                vegetable_counts[veg_name] = quantity
    sorted_vegetables = sorted(vegetable_counts.items())
    result = [f'{veg}={count}' for veg, count in sorted_vegetables]
    return str(result)