def vegetable_counter(order):
    vegetable_counts = {}
    for dish in order:
        # Split the dish by ':' to separate name from ingredients
        _, ingredients = dish.split(':')
        # Split the ingredients by ', '
        ingredients_list = ingredients.split(', ')
        for ingredient in ingredients_list:
            # Split the ingredient by '=' to get the vegetable and its quantity
            vegetable, quantity = ingredient.split('=')
            quantity = int(quantity)
            # Update the count of the vegetable
            if vegetable in vegetable_counts:
                vegetable_counts[vegetable] += quantity
            else:
                vegetable_counts[vegetable] = quantity
    # Sort the vegetables alphabetically and format the output
    sorted_vegetables = sorted(vegetable_counts.items())
    result = [f'{veg}={qty}' for veg, qty in sorted_vegetables]
    return str(result)