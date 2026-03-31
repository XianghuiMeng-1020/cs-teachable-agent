def update_inventory(inventory, sales):
    for game, quantity in sales:
        if game in inventory and inventory[game] >= quantity:
            inventory[game] -= quantity
    return inventory