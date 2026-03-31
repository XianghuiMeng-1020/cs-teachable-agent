def alien_population_change(data):
    population = {}
    for planet, changes in data.items():
        current_population = 1.0
        for change in changes:
            year, change_value = change.split(':')
            current_population += float(change_value) / 1000
        population[planet] = round(current_population, 3)
    return population