def alien_population_change(data):
    populations = {}
    for planet, changes in data.items():
        current_population = 1.0  # starting at 1 million
        for change in changes:
            year, pop_change = change.split(':')
            current_population += float(pop_change) / 1000  # convert to millions
        populations[planet] = round(current_population, 3)  # round to three decimal places
    return populations