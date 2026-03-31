def update_inventory(inventory, sales):
    for game, sold_quantity in sales:
        if game in inventory:
            if inventory[game] >= sold_quantity:
                inventory[game] -= sold_quantity
    return inventory