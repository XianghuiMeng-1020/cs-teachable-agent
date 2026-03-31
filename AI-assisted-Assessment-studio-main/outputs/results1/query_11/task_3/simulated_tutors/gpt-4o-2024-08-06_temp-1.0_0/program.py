def vegetable_counter(order):
    vegetable_totals = {}
    for dish in order:
        # Split the dish into main part and ingredients
        _, ingredients = dish.split(':')
        items = ingredients.split(',')
        for item in items:
            vegetable, quantity = item.split('=')
            vegetable = vegetable.strip()
            quantity = int(quantity.strip())
            if vegetable in vegetable_totals:
                vegetable_totals[vegetable] += quantity
            else:
                vegetable_totals[vegetable] = quantity
    
    # Sort vegetables alphabetically and format them as required
    result = [f"{veg}={qty}" for veg, qty in sorted(vegetable_totals.items())]
    # Convert list to string resembling a dictionary
    return str(result)