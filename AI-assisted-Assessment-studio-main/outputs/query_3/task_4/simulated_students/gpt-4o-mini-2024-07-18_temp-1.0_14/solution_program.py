def classify_planets(data):
    result = {
        'Habitable': [],
        'Potentially Habitable': [],
        'Uninhabitable': []
    }
    for planet in data:
        density = planet['atmos_density']
        life = planet['alien_life']
        name = planet['name']
        if 1.0 <= density <= 3.0:
            if life:
                result['Habitable'].append(name)
            else:
                result['Potentially Habitable'].append(name)
        else:
            result['Uninhabitable'].append(name)
    return result