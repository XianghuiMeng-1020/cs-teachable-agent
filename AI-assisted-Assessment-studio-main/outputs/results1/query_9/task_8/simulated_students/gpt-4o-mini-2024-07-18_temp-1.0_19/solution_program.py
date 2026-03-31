def filter_deities(deities, criteria):
    result = []
    for deity in deities:
        if (not criteria.get('min_strength') or deity['strength'] >= criteria['min_strength']) and  
           (not criteria.get('domain') or deity['domain'] == criteria['domain']):
            result.append(deity['name'])
    return result