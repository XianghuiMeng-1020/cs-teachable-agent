def filter_deities(deities, criteria):
    filtered_names = []
    for deity in deities:
        meets_criteria = True
        if 'min_strength' in criteria:
            if deity['strength'] < criteria['min_strength']:
                meets_criteria = False
        if 'domain' in criteria:
            if deity['domain'] != criteria['domain']:
                meets_criteria = False
        if meets_criteria:
            filtered_names.append(deity['name'])
    return filtered_names