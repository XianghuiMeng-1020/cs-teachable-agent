def alien_population_change(data):
    current_population = {}
    for planet, changes in data.items():
        population = 1.0
        for change in changes:
            year, pop_change = change.split(':')
            population += float(pop_change) / 1000  # Convert change to millions
        current_population[planet] = round(population, 3)
    return current_population