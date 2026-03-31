def mythological_creatures_info(creatures):
    result = {}
    for creature in creatures:
        name = creature['name']
        attributes = creature.get('attributes', {})
        origin = attributes.get('origin', None)
        type_ = attributes.get('type', None)
        strength = attributes.get('strength', 'unknown')
        
        type_strength = None
        if type_ is not None:
            type_strength = f"{type_}: {strength}"
        
        result[name] = {
            'origin': origin,
            'type_strength': [type_strength]
        }
    
    return result

# Example usage
creatures = [
    {'name': 'Minotaur', 'attributes': {'type': 'Beast', 'origin': 'Greece', 'strength': 'High'}},
    {'name': 'Dragon', 'attributes': {'type': 'Reptile', 'origin': 'China'}}
]
print(mythological_creatures_info(creatures))