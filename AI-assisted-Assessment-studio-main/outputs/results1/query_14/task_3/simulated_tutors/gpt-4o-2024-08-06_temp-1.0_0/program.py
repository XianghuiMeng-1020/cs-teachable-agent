def update_pantry(inventory, updates):
    # Helper function to convert string to dictionary
    def parse_items(items_string):
        items = {}  # Dictionary to hold item:quantity pairs
        if items_string:
            for item_qty in items_string.split(','):
                item, qty = item_qty.split(':')
                items[item.strip()] = int(qty.strip())
        return items

    # Helper function to convert dictionary back to string
    def format_items(items_dict):
        items_list = [f"{item}:{qty}" for item, qty in items_dict.items()]
        return ','.join(items_list)

    # Parse the input strings into dictionaries
    inventory_dict = parse_items(inventory)
    updates_dict = parse_items(updates)

    # Apply updates to inventory
    for item, update_qty in updates_dict.items():
        if item in inventory_dict:
            new_qty = inventory_dict[item] + update_qty
            inventory_dict[item] = max(0, new_qty)  # Ensure non-negative quantities

    # Convert the updated inventory dictionary back to a string
    updated_inventory = format_items(inventory_dict)
    return updated_inventory

# Example execution
result = update_pantry('sugar:5,flour:10,olive oil:3', 'sugar:-2,flour:5')
print(result)  # Expected output: 'sugar:3,flour:15,olive oil:3'