def merge_god_items(gods_list):
    item_gods_map = {}
    for god_dict in gods_list:
        for god_name, items in god_dict.items():
            for item in items:
                if item not in item_gods_map:
                    item_gods_map[item] = []
                item_gods_map[item].append(god_name)
    # Sort the list of god names for each item
    for item in item_gods_map:
        item_gods_map[item].sort()
    return item_gods_map