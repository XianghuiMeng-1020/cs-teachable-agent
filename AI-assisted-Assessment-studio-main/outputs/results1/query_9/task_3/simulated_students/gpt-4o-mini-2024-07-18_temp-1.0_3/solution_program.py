def merge_god_items(gods_list):
    items_dict = {}
    for god in gods_list:
        for name, items in god.items():
            for item in items:
                if item not in items_dict:
                    items_dict[item] = []
                items_dict[item].append(name)
    for item in items_dict:
        items_dict[item].sort()
    return items_dict