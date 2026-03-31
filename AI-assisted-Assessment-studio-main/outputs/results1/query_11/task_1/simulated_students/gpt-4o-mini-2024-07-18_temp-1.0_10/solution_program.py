def check_ingredient_availability(ingredients, required_item, required_quantity):
    inventory = {}
    for ingredient in ingredients:
        name, quantity = ingredient.rsplit(' ', 1)
        inventory[name] = int(quantity)
    if required_item in inventory:
        if inventory[required_item] >= required_quantity:
            return 'Available'
    return 'Not Available'