def mythological_creatures_info(creatures):
    info = {}
    for creature in creatures:
        name = creature['name']
        attributes = creature['attributes']
        origin = attributes['origin']
        creature_type = attributes['type']
        strength = attributes.get('strength', 'unknown')
        type_strength = [f'{creature_type}: {strength}']
        info[name] = {'origin': origin, 'type_strength': type_strength}
    return info