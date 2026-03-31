def vegetable_counter(order):
    vegetable_totals = {}

    for dish in order:
        dish_parts = dish.split(':')
        if len(dish_parts) > 1:
            vegetables = dish_parts[1].split(',')
            for veg in vegetables:
                veg_name, quantity = veg.split('=')
                veg_name = veg_name.strip()
                quantity = int(quantity.strip())
                if veg_name in vegetable_totals:
                    vegetable_totals[veg_name] += quantity
                else:
                    vegetable_totals[veg_name] = quantity

    sorted_vegetables = sorted(vegetable_totals.items())
    result = [f'{veg}={quantity}' for veg, quantity in sorted_vegetables]

    return str(result)