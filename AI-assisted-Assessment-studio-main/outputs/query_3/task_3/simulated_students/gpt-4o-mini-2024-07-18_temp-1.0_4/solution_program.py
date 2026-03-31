def alien_population_change(data):
    current_population = {}
    for planet, changes in data.items():
        population = 1.0  # starting at 1 million
        for change in changes:
            year, change_value = change.split(':')
            population += int(change_value) / 1000  # convert change from thousands to millions
        current_population[planet] = round(population, 3)  # round to 3 decimal places
    return current_population