def update_pantry(inventory, updates):
    pantry = {item.split(':')[0]: int(item.split(':')[1]) for item in inventory.split(',')}
    update_list = updates.split(',')

    for update in update_list:
        item, quantity_change = update.split(':')
        quantity_change = int(quantity_change)
        pantry[item] += quantity_change
        if pantry[item] < 0:
            pantry[item] = 0

    updated_inventory = []
    for item in inventory.split(','):
        item_name = item.split(':')[0]
        updated_inventory.append(f"{item_name}:{pantry[item_name]}")

    return ','.join(updated_inventory)