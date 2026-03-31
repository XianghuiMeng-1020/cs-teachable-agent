def classify_planets(data):
    categories = {'Habitable': [], 'Potentially Habitable': [], 'Uninhabitable': []}

    for planet in data:
        density = planet['atmos_density']
        alien_life = planet['alien_life']

        if 1.0 <= density <= 3.0:
            if alien_life:
                categories['Habitable'].append(planet['name'])
            else:
                categories['Potentially Habitable'].append(planet['name'])
        else:
            categories['Uninhabitable'].append(planet['name'])

    return categories