def filter_deities(deities, criteria):
    results = []
    for deity in deities:
        matches = True
        if 'min_strength' in criteria:
            if deity['strength'] < criteria['min_strength']:
                matches = False
        if 'domain' in criteria:
            if deity['domain'] != criteria['domain']:
                matches = False
        if matches:
            results.append(deity['name'])
    return results