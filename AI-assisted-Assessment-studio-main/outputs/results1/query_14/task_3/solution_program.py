def update_pantry(inventory, updates):
    inv_dict = {}
    updates_dict = {}
    for item in inventory.split(','):
        name, quantity = item.split(':')
        inv_dict[name] = int(quantity)
    for update in updates.split(','):
        if update:
            name, change = update.split(':')
            updates_dict[name] = int(change)
    for name, change in updates_dict.items():
        if name in inv_dict:
            inv_dict[name] += change
            if inv_dict[name] < 0:
                inv_dict[name] = 0
    return ','.join(f'{name}:{quantity}' for name, quantity in inv_dict.items())