def update_pantry(inventory, updates):
    pantry = {}
    # Split the initial inventory into items and quantities
    for item in inventory.split(','):
        name, quantity = item.split(':')
        pantry[name] = int(quantity)
    # Apply updates to the pantry
    for update in updates.split(','):
        name, change = update.split(':')
        pantry[name] += int(change)
        # Ensure quantity does not go below zero
        if pantry[name] < 0:
            pantry[name] = 0
    # Create the updated inventory string
    updated_inventory = []
    for item in inventory.split(','):
        name = item.split(':')[0]
        updated_inventory.append(f'{name}:{pantry[name]}')
    return ','.join(updated_inventory)