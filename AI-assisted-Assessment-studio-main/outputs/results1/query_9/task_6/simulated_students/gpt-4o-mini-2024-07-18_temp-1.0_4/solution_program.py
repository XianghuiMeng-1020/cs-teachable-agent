def mythological_creatures_info(creatures):
    result = {}
    
    for creature in creatures:
        name = creature['name']
        attributes = creature['attributes']
        origin = attributes['origin']
        creature_type = attributes['type']
        strength = attributes.get('strength', 'unknown')
        
        result[name] = {
            'origin': origin,
            'type_strength': [f'{creature_type}: {strength}']
        }
    
    return result