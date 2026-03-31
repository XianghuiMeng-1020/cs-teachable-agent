def update_pantry(inventory, updates):
    pantry = dict(item.split(':') for item in inventory.split(','))
    updates_dict = dict(item.split(':') for item in updates.split(','))
    
    for item, change in updates_dict.items():
        current_quantity = int(pantry[item])
        new_quantity = current_quantity + int(change)
        pantry[item] = max(new_quantity, 0)
    
    updated_inventory = ','.join(f'{item}:{pantry[item]}' for item in pantry)
    return updated_inventory