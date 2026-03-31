def alien_population_change(data):
    population = {}
    for planet, changes in data.items():
        current_population = 1.0
        for change in changes:
            year, pop_change = change.split(':')
            current_population += float(pop_change) / 1000
        population[planet] = round(current_population, 3)
    return population