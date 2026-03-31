def vegetable_counter(order):
    vegetable_totals = {}
    
    for dish in order:
        _, vegetables_str = dish.split(': ')
        vegetables = vegetables_str.split(', ')
        
        for vegetable in vegetables:
            veg_name, quantity = vegetable.split('=')
            quantity = int(quantity)
            
            if veg_name in vegetable_totals:
                vegetable_totals[veg_name] += quantity
            else:
                vegetable_totals[veg_name] = quantity
    
    sorted_vegetables = sorted(vegetable_totals.items())
    result = [f'{veg}={qty}' for veg, qty in sorted_vegetables]
    return str(result)