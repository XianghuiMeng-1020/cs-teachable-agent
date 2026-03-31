def classify_planets(data):
    classification = {'Habitable': [], 'Potentially Habitable': [], 'Uninhabitable': []}
    for planet in data:
        density = planet['atmos_density']
        alien_life = planet['alien_life']
        if 1.0 <= density <= 3.0:
            if alien_life:
                classification['Habitable'].append(planet['name'])
            else:
                classification['Potentially Habitable'].append(planet['name'])
        else:
            classification['Uninhabitable'].append(planet['name'])
    return classification