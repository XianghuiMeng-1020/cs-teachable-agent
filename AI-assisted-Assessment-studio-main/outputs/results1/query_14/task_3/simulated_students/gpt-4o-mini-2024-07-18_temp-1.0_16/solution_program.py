def update_pantry(inventory, updates):
    pantry = {}
    for item in inventory.split(','):
        name, quantity = item.split(':')
        pantry[name] = int(quantity)

    for update in updates.split(','):
        name, change = update.split(':')
        pantry[name] += int(change)
        if pantry[name] < 0:
            pantry[name] = 0

    updated_inventory = []
    for item in inventory.split(','):
        name = item.split(':')[0]
        updated_inventory.append(f'{name}:{pantry[name]}')

    return ','.join(updated_inventory)