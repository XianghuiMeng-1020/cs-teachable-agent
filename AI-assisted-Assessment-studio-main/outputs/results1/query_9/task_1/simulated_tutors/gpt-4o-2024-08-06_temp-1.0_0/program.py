def count_gods_attributes(gods_list):
    attribute_count = {}
    for god in gods_list:
        for attribute in god['attributes']:
            if attribute in attribute_count:
                attribute_count[attribute] += 1
            else:
                attribute_count[attribute] = 1
    return attribute_count

gods_list = [
    {"name": "zeus", "attributes": ["thunder", "sky", "justice"]},
    {"name": "hera", "attributes": ["marriage", "sky", "womanhood"]},
    {"name": "poseidon", "attributes": ["sea", "horses", "earthquake"]},
    {"name": "athena", "attributes": ["wisdom", "war", "justice"]},
]

# Example call
gods_attributes_count = count_gods_attributes(gods_list)
print(gods_attributes_count)