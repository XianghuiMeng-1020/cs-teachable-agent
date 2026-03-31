def filter_deities(deities, criteria):
    if not criteria:
        return [deity['name'] for deity in deities]

    filtered_deities = deities

    if 'min_strength' in criteria:
        min_strength = criteria['min_strength']
        filtered_deities = [deity for deity in filtered_deities if deity['strength'] >= min_strength]

    if 'domain' in criteria:
        domain = criteria['domain']
        filtered_deities = [deity for deity in filtered_deities if deity['domain'] == domain]

    return [deity['name'] for deity in filtered_deities]