def update_pantry(inventory, updates):
    pantry = {item.split(':')[0]: int(item.split(':')[1]) for item in inventory.split(',')}

    for update in updates.split(','):
        item, change = update.split(':')
        pantry[item] += int(change)
        if pantry[item] < 0:
            pantry[item] = 0

    return ','.join(f'{item}:{pantry[item]}' for item in inventory.split(','))