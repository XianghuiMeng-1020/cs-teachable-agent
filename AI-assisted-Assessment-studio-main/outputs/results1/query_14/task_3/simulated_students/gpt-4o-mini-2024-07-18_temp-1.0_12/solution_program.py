def update_pantry(inventory, updates):
    pantry = dict(item.split(':') for item in inventory.split(','))
    for update in updates.split(','):
        item, change = update.split(':')
        pantry[item] = max(0, int(pantry[item]) + int(change))
    return ','.join(f'{item}:{pantry[item]}' for item in pantry)