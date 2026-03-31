def update_pantry(inventory, updates):
    pantry = dict(item.split(':') for item in inventory.split(','))
    update_items = dict(item.split(':') for item in updates.split(','))

    for item, change in update_items.items():
        pantry[item] = max(0, int(pantry[item]) + int(change))

    return ','.join(f'{item}:{pantry[item]}' for item in inventory.split(','))