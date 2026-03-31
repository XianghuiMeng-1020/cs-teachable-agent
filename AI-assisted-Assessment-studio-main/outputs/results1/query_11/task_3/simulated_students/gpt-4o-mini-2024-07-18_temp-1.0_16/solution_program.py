def vegetable_counter(order):
    vegetable_count = {}
    for dish in order:
        dish_parts = dish.split(':')
        if len(dish_parts) > 1:
            vegs = dish_parts[1].split(',')
            for veg in vegs:
                veg_name, quantity = veg.split('=')
                quantity = int(quantity)
                veg_name = veg_name.strip()
                if veg_name in vegetable_count:
                    vegetable_count[veg_name] += quantity
                else:
                    vegetable_count[veg_name] = quantity
    sorted_vegetables = sorted(vegetable_count.items())
    result = [f'{name}={quantity}' for name, quantity in sorted_vegetables]
    return str(result)