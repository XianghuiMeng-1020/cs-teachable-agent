def check_ingredient_availability(ingredients, required_item, required_quantity):
    available_quantity = 0
    for ingredient in ingredients:
        name, quantity = ingredient.rsplit(' ', 1)
        if name == required_item:
            available_quantity = int(quantity)
            break
    return 'Available' if available_quantity >= required_quantity else 'Not Available'