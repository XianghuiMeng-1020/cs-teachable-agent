def check_ingredient_availability(ingredients, required_item, required_quantity):
    inventory = {item.split()[0]: int(item.split()[1]) for item in ingredients}
    if required_item in inventory and inventory[required_item] >= required_quantity:
        return 'Available'
    else:
        return 'Not Available'