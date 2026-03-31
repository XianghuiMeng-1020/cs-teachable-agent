def update_pantry(inventory, updates):
    # Convert the inventory string to a dictionary
    pantry = dict(item.split(':') for item in inventory.split(','))
    # Convert values to integers
    for item in pantry:
        pantry[item] = int(pantry[item])

    # Update the pantry with the updates
    for update in updates.split(','):
        item, change = update.split(':')
        change = int(change)
        # Apply the change and ensure quantity doesn't go below zero
        pantry[item] += change
        if pantry[item] < 0:
            pantry[item] = 0

    # Prepare the updated inventory string
    updated_inventory = ','.join(f'{item}:{pantry[item]}' for item in pantry)
    return updated_inventory