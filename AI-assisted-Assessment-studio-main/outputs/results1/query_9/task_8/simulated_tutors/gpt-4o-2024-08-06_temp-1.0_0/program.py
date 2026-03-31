def filter_deities(deities, criteria):
    min_strength = criteria.get('min_strength', -1)
    domain = criteria.get('domain', None)

    filtered_names = []
    for deity in deities:
        if deity['strength'] >= min_strength:
            if domain is None or deity['domain'] == domain:
                filtered_names.append(deity['name'])

    return filtered_names