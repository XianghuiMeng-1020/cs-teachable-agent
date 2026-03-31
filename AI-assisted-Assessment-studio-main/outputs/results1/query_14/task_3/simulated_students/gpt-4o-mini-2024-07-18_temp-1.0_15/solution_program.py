def update_pantry(inventory, updates):
    pantry = {item.split(':')[0]: int(item.split(':')[1]) for item in inventory.split(',')}
    updates_dict = {item.split(':')[0]: int(item.split(':')[1]) for item in updates.split(',')}

    for item, quantity in updates_dict.items():
        pantry[item] += quantity
        if pantry[item] < 0:
            pantry[item] = 0

    updated_inventory = ','.join(f'{item}:{pantry[item]}' for item in pantry)
    return updated_inventory