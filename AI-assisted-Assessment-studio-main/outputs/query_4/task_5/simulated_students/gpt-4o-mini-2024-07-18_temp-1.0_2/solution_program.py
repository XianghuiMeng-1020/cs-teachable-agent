def update_inventory(inventory, sales):
    for sale in sales:
        game_name, quantity_sold = sale
        if game_name in inventory:
            if inventory[game_name] >= quantity_sold:
                inventory[game_name] -= quantity_sold
    return inventory