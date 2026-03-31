def vegetable_counter(order):
    vegetable_totals = {}
    
    for dish in order:
        dish_info = dish.split(':')
        if len(dish_info) > 1:
            vegetables = dish_info[1].split(',')
            for vegetable in vegetables:
                veg_info = vegetable.split('=')
                if len(veg_info) == 2:
                    name = veg_info[0].strip()
                    quantity = int(veg_info[1].strip())
                    if name in vegetable_totals:
                        vegetable_totals[name] += quantity
                    else:
                        vegetable_totals[name] = quantity
    
    sorted_vegetables = sorted(vegetable_totals.items())
    result = [f'{name}={quantity}' for name, quantity in sorted_vegetables]
    
    return str(result)