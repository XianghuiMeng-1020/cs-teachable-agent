def mythical_population_info(creatures):
    total_creatures = len(creatures)
    if total_creatures == 0:
        return {
            'total_creatures': 0,
            'average_power': 0,
            'kingdom_distribution': {}
        }
    
    total_power = 0
    kingdom_distribution = {}
    
    for creature in creatures:
        total_power += creature['power']
        kingdom = creature['kingdom']
        if kingdom in kingdom_distribution:
            kingdom_distribution[kingdom] += 1
        else:
            kingdom_distribution[kingdom] = 1
    
    average_power = total_power // total_creatures  # Integer division
    
    return {
        'total_creatures': total_creatures,
        'average_power': average_power,
        'kingdom_distribution': kingdom_distribution
    }

# Example usage:
creatures = [
    {'name': 'Zeus', 'kingdom': 'Olympus', 'power': 100},
    {'name': 'Hades', 'kingdom': 'Underworld', 'power': 95},
    {'name': 'Poseidon', 'kingdom': 'Ocean', 'power': 90},
    {'name': 'Athena', 'kingdom': 'Olympus', 'power': 85}
]

print(mythical_population_info(creatures))