def update_inventory(inventory, sales):
    for game_name, quantity_sold in sales:
        if game_name in inventory:
            # Check if there is enough stock to process the sale
            if inventory[game_name] >= quantity_sold:
                # Update the inventory by reducing the sold quantity
                inventory[game_name] -= quantity_sold
    return inventory

# Example usage
inventory = {
    'Monopoly': 5,
    'Risk': 7,
    'Catan': 3
}
sales = [
    ('Monopoly', 2),
    ('Risk', 8),
    ('Catan', 1)
]

updated_inventory = update_inventory(inventory, sales)
print(updated_inventory)  # Output should be {'Monopoly': 3, 'Risk': 7, 'Catan': 2}
