def count_gods_attributes(gods_list):
    attributes_count = {}
    for god in gods_list:
        for attribute in god['attributes']:  
            if attribute in attributes_count:
                attributes_count[attribute] += 1
            else:
                attributes_count[attribute] = 1
    return attributes_count