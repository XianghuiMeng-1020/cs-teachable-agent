def merge_god_items(gods_list):
    item_to_gods = {}
    
    for god_dict in gods_list:
        for god, items in god_dict.items():
            for item in items:
                if item not in item_to_gods:
                    item_to_gods[item] = []
                item_to_gods[item].append(god)
    
    for item in item_to_gods:
        item_to_gods[item].sort()
    
    return item_to_gods