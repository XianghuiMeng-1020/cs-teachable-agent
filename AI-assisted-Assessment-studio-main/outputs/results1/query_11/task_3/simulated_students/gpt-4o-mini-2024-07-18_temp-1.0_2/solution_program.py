def vegetable_counter(order):
    vegetable_totals = {}
    
    for dish in order:
        _, veggies = dish.split(':')
        veggies = veggies.split(',')
        
        for veggie in veggies:
            name, quantity = veggie.split('=')
            name = name.strip()
            quantity = int(quantity.strip())
            
            if name in vegetable_totals:
                vegetable_totals[name] += quantity
            else:
                vegetable_totals[name] = quantity
    
    sorted_vegetables = sorted(vegetable_totals.items())
    result = [f'{name}={qty}' for name, qty in sorted_vegetables]
    return str(result)