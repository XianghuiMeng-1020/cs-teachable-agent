def vegetable_counter(order):
    vegetable_totals = {}
    for dish in order:
        dish_parts = dish.split(':')
        vegetables = dish_parts[1].strip().split(', ')
        for veg in vegetables:
            veg_name, quantity = veg.split('=')
            veg_name = veg_name.strip()
            quantity = int(quantity.strip())
            if veg_name in vegetable_totals:
                vegetable_totals[veg_name] += quantity
            else:
                vegetable_totals[veg_name] = quantity
    sorted_vegetables = sorted(vegetable_totals.items())
    output = [f'{veg}={qty}' for veg, qty in sorted_vegetables]
    return str(output)