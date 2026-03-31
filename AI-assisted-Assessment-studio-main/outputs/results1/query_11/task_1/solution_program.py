def check_ingredient_availability(ingredients, required_item, required_quantity):
    for ingredient in ingredients:
        name, quantity = ingredient.split()
        quantity = int(quantity)
        if name == required_item:
            if quantity >= required_quantity:
                return 'Available'
            else:
                return 'Not Available'
    return 'Not Available'