def filter_deities(deities, criteria):
    if not criteria:
        return [deity['name'] for deity in deities]
    filtered_deities = []
    for deity in deities:
        matches = True
        if 'min_strength' in criteria:
            if deity['strength'] < criteria['min_strength']:
                matches = False
        if 'domain' in criteria:
            if deity['domain'] != criteria['domain']:
                matches = False
        if matches:
            filtered_deities.append(deity['name'])
    return filtered_deities