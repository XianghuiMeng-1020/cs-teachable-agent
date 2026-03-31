def filter_deities(deities, criteria):
    filtered_deities = []
    for deity in deities:
        match = True
        if 'min_strength' in criteria:
            if deity['strength'] < criteria['min_strength']:
                match = False
        if 'domain' in criteria:
            if deity['domain'] != criteria['domain']:
                match = False
        if match:
            filtered_deities.append(deity['name'])
    return filtered_deities if filtered_deities else []
