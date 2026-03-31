def update_pantry(inventory, updates):
    # Convert inventory to a dictionary
    pantry = {}
    for item in inventory.split(','):
        name, quantity = item.split(':')
        pantry[name] = int(quantity)

    # Process updates
    for item in updates.split(','):
        name, change = item.split(':')
        change = int(change)
        pantry[name] += change
        # Ensure quantity is non-negative
        if pantry[name] < 0:
            pantry[name] = 0

    # Build the updated inventory string
    updated_inventory = []
    for item in inventory.split(','):
        name = item.split(':')[0]
        updated_inventory.append(f'{name}:{pantry[name]}')

    return ','.join(updated_inventory)