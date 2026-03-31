def filter_deities(deities, criteria):
    filtered_deities = []
    for deity in deities:
        if ('min_strength' in criteria and deity['strength'] < criteria['min_strength']):
            continue
        if ('domain' in criteria and deity['domain'] != criteria['domain']):
            continue
        filtered_deities.append(deity['name'])
    return filtered_deities