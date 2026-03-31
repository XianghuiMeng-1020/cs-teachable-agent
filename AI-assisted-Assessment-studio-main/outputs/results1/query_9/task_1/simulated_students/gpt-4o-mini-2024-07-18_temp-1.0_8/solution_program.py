def count_gods_attributes(gods_list):
    attribute_count = {}
    
    for god in gods_list:
        for attribute in god['attributes']:
            if attribute in attribute_count:
                attribute_count[attribute] += 1
            else:
                attribute_count[attribute] = 1
    
    return attribute_count