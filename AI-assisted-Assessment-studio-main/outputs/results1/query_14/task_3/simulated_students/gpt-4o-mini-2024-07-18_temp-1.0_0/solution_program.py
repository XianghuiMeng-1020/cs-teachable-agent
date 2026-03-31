def update_pantry(inventory, updates):
    pantry = {}
    for item in inventory.split(','):
        key, value = item.split(':')
        pantry[key] = int(value)
    for update in updates.split(','):
        key, value = update.split(':')
        pantry[key] += int(value)
        if pantry[key] < 0:
            pantry[key] = 0
    updated_inventory = []
    for item in inventory.split(','):
        key = item.split(':')[0]
        updated_inventory.append(f'{key}:{pantry[key]}')
    return ','.join(updated_inventory)