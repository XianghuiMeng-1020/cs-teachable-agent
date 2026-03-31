def update_pantry(inventory, updates):
    # Parse the inventory string into a dictionary
    inventory_dict = {}
    for item in inventory.split(','):
        name, quantity = item.split(':')
        inventory_dict[name] = int(quantity)
    
    # Parse the updates string and apply the changes
    for update in updates.split(','):
        name, change = update.split(':')
        change_value = int(change)
        if name in inventory_dict:
            inventory_dict[name] += change_value
            # Ensure the quantity does not fall below zero
            if inventory_dict[name] < 0:
                inventory_dict[name] = 0
    
    # Create the updated inventory string
    updated_inventory = []
    for item in inventory.split(','):
        name, _ = item.split(':')
        updated_inventory.append(f'{name}:{inventory_dict[name]}')
    
    return ','.join(updated_inventory)