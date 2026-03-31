def update_pantry(inventory, updates):
    inventory_dict = {item.split(':')[0]: int(item.split(':')[1]) for item in inventory.split(',')}
    updates_dict = {item.split(':')[0]: int(item.split(':')[1]) for item in updates.split(',')}
    
    for item, change in updates_dict.items():
        new_quantity = inventory_dict[item] + change
        inventory_dict[item] = max(new_quantity, 0)
    
    updated_inventory = [f'{item}:{inventory_dict[item]}' for item in inventory_dict]
    
    return ','.join(updated_inventory)