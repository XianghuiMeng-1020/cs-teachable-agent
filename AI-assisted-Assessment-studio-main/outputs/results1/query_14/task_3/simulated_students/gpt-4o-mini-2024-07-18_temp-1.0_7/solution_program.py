def update_pantry(inventory, updates):
    # Parse the current inventory
    pantry = {item.split(':')[0]: int(item.split(':')[1]) for item in inventory.split(',')}
    # Parse the updates
    updates_list = updates.split(',')
    for update in updates_list:
        item, change = update.split(':')
        # Update the pantry with the changes
        pantry[item] += int(change)
        # Ensure quantities are not negative
        if pantry[item] < 0:
            pantry[item] = 0
    # Prepare the final output in the same order as inventory
    updated_inventory = ','.join([f'{item}:{pantry[item]}' for item in pantry])
    return updated_inventory