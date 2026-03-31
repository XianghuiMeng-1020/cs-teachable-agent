def update_pantry(inventory, updates):
    # Convert inventory string to a dictionary
    pantry = {item.split(':')[0]: int(item.split(':')[1]) for item in inventory.split(',')}
    
    # Process the updates
    for update in updates.split(','):
        item, quantity_change = update.split(':')
        quantity_change = int(quantity_change)
        
        # Update the pantry with non-negative quantities
        pantry[item] = max(0, pantry[item] + quantity_change)
    
    # Construct the updated inventory string
    updated_inventory = ','.join([f'{item}:{pantry[item]}' for item in pantry])
    
    return updated_inventory