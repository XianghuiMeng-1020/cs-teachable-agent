def count_gods_attributes(gods_list):
    attribute_counts = {}
    for god in gods_list:
        for attribute in god['attributes']:
            if attribute in attribute_counts:
                attribute_counts[attribute] += 1
            else:
                attribute_counts[attribute] = 1
    return attribute_counts