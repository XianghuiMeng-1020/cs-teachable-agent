def alien_population_change(data):
    population = {}
    for planet, changes in data.items():
        current_population = 1.0  # Starting population in millions
        for change in changes:
            year, change_value = change.split(':')
            current_population += float(change_value) / 1000
        population[planet] = round(current_population, 3)  # Round to 3 decimal places
    return population