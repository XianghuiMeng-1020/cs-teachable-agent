def update_pantry(inventory, updates):
    # Create a dictionary from the inventory
    pantry = {}
    for item in inventory.split(','):
        name, quantity = item.split(':')
        pantry[name] = int(quantity)

    # Update the pantry with the updates
    for update in updates.split(','):
        name, change = update.split(':')
        change = int(change)
        pantry[name] += change
        # Ensure the quantity does not fall below zero
        if pantry[name] < 0:
            pantry[name] = 0

    # Create the resulting inventory string in the same order
    updated_inventory = []
    for item in inventory.split(','):
        name = item.split(':')[0]
        updated_inventory.append(f'{name}:{pantry[name]}')

    return ','.join(updated_inventory)