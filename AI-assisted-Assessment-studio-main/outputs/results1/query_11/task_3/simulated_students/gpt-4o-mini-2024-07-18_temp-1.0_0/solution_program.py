def vegetable_counter(order):
    vegetable_count = {}
    
    for dish in order:
        # Split the string into dish name and ingredients part
        ingredients_part = dish.split(':')[1]
        # Split the ingredients part into individual ingredients
        ingredients = ingredients_part.split(', ')
        
        for ingredient in ingredients:
            # Split each ingredient into vegetable and quantity
            vegetable, quantity = ingredient.split('=')
            quantity = int(quantity)
            
            # Add quantity to the vegetable count
            if vegetable in vegetable_count:
                vegetable_count[vegetable] += quantity
            else:
                vegetable_count[vegetable] = quantity
    
    # Create a sorted list of vegetable quantities as strings
    sorted_vegetables = sorted(vegetable_count.items())
    result = [f'{vegetable}={count}' for vegetable, count in sorted_vegetables]
    
    return str(result)