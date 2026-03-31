def mythical_population_info(creatures):
    total_creatures = len(creatures)
    total_power = sum(creature['power'] for creature in creatures)
    average_power = total_power // total_creatures if total_creatures > 0 else 0
    kingdom_distribution = {}

    for creature in creatures:
        kingdom = creature['kingdom']
        if kingdom in kingdom_distribution:
            kingdom_distribution[kingdom] += 1
        else:
            kingdom_distribution[kingdom] = 1

    return {
        'total_creatures': total_creatures,
        'average_power': average_power,
        'kingdom_distribution': kingdom_distribution,
    }