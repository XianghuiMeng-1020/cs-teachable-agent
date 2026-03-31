def merge_god_items(gods_list):
    item_to_gods = {}
    
    for god in gods_list:
        for name, items in god.items():
            for item in items:
                if item not in item_to_gods:
                    item_to_gods[item] = []
                item_to_gods[item].append(name)
    
    for item in item_to_gods:
        item_to_gods[item].sort()
    
    return item_to_gods