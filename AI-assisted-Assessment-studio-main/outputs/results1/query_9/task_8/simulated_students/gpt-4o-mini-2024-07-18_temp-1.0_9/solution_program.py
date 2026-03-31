def filter_deities(deities, criteria):
    if not criteria:
        return [deity['name'] for deity in deities]

    filtered_deities = deities

    if 'min_strength' in criteria:
        filtered_deities = [deity for deity in filtered_deities if deity['strength'] >= criteria['min_strength']]
    
    if 'domain' in criteria:
        filtered_deities = [deity for deity in filtered_deities if deity['domain'] == criteria['domain']]
    
    return [deity['name'] for deity in filtered_deities]