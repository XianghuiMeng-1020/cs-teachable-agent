def merge_god_items(gods_list):
    merged_items = {}
    for god in gods_list:
        for name, items in god.items():
            for item in items:
                if item not in merged_items:
                    merged_items[item] = []
                merged_items[item].append(name)
    for item in merged_items:
        merged_items[item].sort()
    return merged_items