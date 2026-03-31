def merge_god_items(gods_list):
    merged_items = {}
    
    for god_dict in gods_list:
        for god, items in god_dict.items():
            for item in items:
                if item not in merged_items:
                    merged_items[item] = []
                merged_items[item].append(god)
    
    for item in merged_items:
        merged_items[item].sort()
    
    return merged_items