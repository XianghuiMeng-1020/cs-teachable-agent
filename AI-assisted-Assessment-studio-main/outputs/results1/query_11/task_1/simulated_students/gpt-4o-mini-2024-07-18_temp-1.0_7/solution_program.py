def check_ingredient_availability(ingredients, required_item, required_quantity):
    inventory = {}
    for item in ingredients:
        name, quantity = item.rsplit(' ', 1)
        inventory[name] = int(quantity)
    if required_item in inventory and inventory[required_item] >= required_quantity:
        return 'Available'
    else:
        return 'Not Available'