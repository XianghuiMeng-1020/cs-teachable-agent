def alien_population_change(data):
    current_population = {}
    for planet, changes in data.items():
        population = 1.0  # Starting population in millions
        for change in changes:
            year, change_amount = change.split(':')
            population += int(change_amount) / 1000  # Convert change from thousands to millions
        current_population[planet] = round(population, 3)  # Round to 3 decimal places
    return current_population