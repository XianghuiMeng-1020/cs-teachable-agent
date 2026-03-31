def mythological_creatures_info(creatures):
    result = {}
    for creature in creatures:
        name = creature['name']
        attributes = creature['attributes']
        creature_origin = attributes.get('origin', None)
        creature_type = attributes.get('type', None)
        creature_strength = attributes.get('strength', 'unknown')
        if creature_type:
            type_strength = [f"{creature_type}: {creature_strength}"]
        else:
            type_strength = [None]
        result[name] = {
            'origin': creature_origin,
            'type_strength': type_strength
        }
    return result
