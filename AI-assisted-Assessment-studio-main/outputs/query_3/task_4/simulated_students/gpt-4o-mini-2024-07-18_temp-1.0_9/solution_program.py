def classify_planets(data):
    classifications = {'Habitable': [], 'Potentially Habitable': [], 'Uninhabitable': []}
    
    for planet in data:
        density = planet['atmos_density']
        has_alien_life = planet['alien_life']
        
        if 1.0 <= density <= 3.0:
            if has_alien_life:
                classifications['Habitable'].append(planet['name'])
            else:
                classifications['Potentially Habitable'].append(planet['name'])
        else:
            classifications['Uninhabitable'].append(planet['name'])
    
    return classifications