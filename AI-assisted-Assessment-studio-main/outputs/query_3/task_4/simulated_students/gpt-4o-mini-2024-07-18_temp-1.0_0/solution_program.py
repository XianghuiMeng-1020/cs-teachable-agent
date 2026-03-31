def classify_planets(data):
    categories = {'Habitable': [], 'Potentially Habitable': [], 'Uninhabitable': []}
    
    for planet in data:
        density = planet['atmos_density']
        if 1.0 <= density <= 3.0:
            if planet['alien_life']:
                categories['Habitable'].append(planet['name'])
            else:
                categories['Potentially Habitable'].append(planet['name'])
        else:
            categories['Uninhabitable'].append(planet['name'])
    
    return categories