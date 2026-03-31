def classify_planets(data):
    classification = {
        'Habitable': [],
        'Potentially Habitable': [],
        'Uninhabitable': []
    }
    
    for planet in data:
        name = planet['name']
        density = planet['atmos_density']
        alien_life = planet['alien_life']
        
        if 1.0 <= density <= 3.0:
            if alien_life:
                classification['Habitable'].append(name)
            else:
                classification['Potentially Habitable'].append(name)
        else:
            classification['Uninhabitable'].append(name)
    
    return classification

# Sample test run
planets = [
    {'name': 'Zorgon', 'atmos_density': 2.5, 'alien_life': True},
    {'name': 'Arion', 'atmos_density': 3.1, 'alien_life': False},
    {'name': 'Lorca', 'atmos_density': 1.8, 'alien_life': False},
    {'name': 'Blip', 'atmos_density': 0.9, 'alien_life': True},
]

result = classify_planets(planets)
print(result)