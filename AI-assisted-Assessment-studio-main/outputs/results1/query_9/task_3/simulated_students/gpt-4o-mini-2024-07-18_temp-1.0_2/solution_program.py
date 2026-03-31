def merge_god_items(gods_list):
    item_god_map = {}
    
    for god_dict in gods_list:
        for god, items in god_dict.items():
            for item in items:
                if item not in item_god_map:
                    item_god_map[item] = []
                item_god_map[item].append(god)

    # Sort the list of gods for each item
    for item in item_god_map:
        item_god_map[item].sort()

    return item_god_map