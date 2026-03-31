def merge_god_items(gods_list):
    item_god_map = {}
    
    for god_items in gods_list:
        for god, items in god_items.items():
            for item in items:
                if item not in item_god_map:
                    item_god_map[item] = []
                item_god_map[item].append(god)
    
    for item in item_god_map:
        item_god_map[item] = sorted(item_god_map[item])
    
    return item_god_map