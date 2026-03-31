def update_inventory(inventory, sales):
    for game, quantity_sold in sales:
        if game in inventory:
            if inventory[game] >= quantity_sold:
                inventory[game] -= quantity_sold
    return inventory