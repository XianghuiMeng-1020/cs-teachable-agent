def merge_god_items(gods_list):
    item_to_gods = {}
    
    for god_dict in gods_list:
        for god, items in god_dict.items():
            for item in items:
                if item not in item_to_gods:
                    item_to_gods[item] = []
                item_to_gods[item].append(god)

    # Sort the list of gods for each item alphabetically
    for item in item_to_gods:
        item_to_gods[item].sort()

    return item_to_gods

# Example usage
input_gods = [
    {'Zeus': ['thunderbolt', 'eagle']},
    {'Athena': ['owl', 'shield', 'thunderbolt']},
    {'Ares': ['spear', 'shield']}
]

result = merge_god_items(input_gods)
print(result)