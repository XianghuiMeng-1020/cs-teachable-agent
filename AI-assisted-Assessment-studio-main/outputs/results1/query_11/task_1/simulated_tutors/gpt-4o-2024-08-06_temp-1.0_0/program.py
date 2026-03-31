def check_ingredient_availability(ingredients, required_item, required_quantity):
    for ingredient in ingredients:
        name, available_quantity = ingredient.rsplit(' ', 1)
        if name == required_item:
            if int(available_quantity) >= required_quantity:
                return 'Available'
            else:
                return 'Not Available'
    return 'Not Available'