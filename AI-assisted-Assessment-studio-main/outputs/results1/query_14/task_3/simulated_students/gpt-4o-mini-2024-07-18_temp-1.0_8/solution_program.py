def update_pantry(inventory, updates):
    # Convert the inventory string to a dictionary for easier manipulation
    pantry = {item.split(':')[0]: int(item.split(':')[1]) for item in inventory.split(',')}

    # Process the updates
    for update in updates.split(','):
        item, change = update.split(':')
        # Update the quantity, ensure it does not go below zero
        pantry[item] = max(0, pantry[item] + int(change))

    # Recreate the inventory string in the original format
    updated_inventory = ','.join(f'{item}:{quantity}' for item, quantity in pantry.items())
    return updated_inventory