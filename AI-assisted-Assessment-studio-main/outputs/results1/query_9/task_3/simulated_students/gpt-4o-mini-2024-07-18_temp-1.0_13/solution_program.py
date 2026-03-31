def merge_god_items(gods_list):
    item_gods = {}
    
    for god in gods_list:
        for name, items in god.items():
            for item in items:
                if item not in item_gods:
                    item_gods[item] = []
                item_gods[item].append(name)
                
    for item in item_gods:
        item_gods[item].sort()  
    
    return item_gods