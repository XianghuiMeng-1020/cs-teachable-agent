def classify_planets(data):
    classified_planets = {'Habitable': [], 'Potentially Habitable': [], 'Uninhabitable': []}
    
    for planet in data:
        name = planet['name']
        density = planet['atmos_density']
        alien_life = planet['alien_life']
        
        if 1.0 <= density <= 3.0:
            if alien_life:
                classified_planets['Habitable'].append(name)
            else:
                classified_planets['Potentially Habitable'].append(name)
        else:
            classified_planets['Uninhabitable'].append(name)
    
    return classified_planets