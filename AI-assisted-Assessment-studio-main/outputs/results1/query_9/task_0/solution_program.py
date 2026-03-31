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
        if kingdom not in kingdom_distribution:
            kingdom_distribution[kingdom] = 0
        kingdom_distribution[kingdom] += 1
    average_power = total_power // total_creatures
    return {
        'total_creatures': total_creatures,
        'average_power': average_power,
        'kingdom_distribution': kingdom_distribution
    }