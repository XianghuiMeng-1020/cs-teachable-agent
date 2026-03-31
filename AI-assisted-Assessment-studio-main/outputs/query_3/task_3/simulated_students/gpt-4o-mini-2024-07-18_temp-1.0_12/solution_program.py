def alien_population_change(data):
    final_population = {}
    for planet, changes in data.items():
        population = 1.0  # Starting population in millions
        for entry in changes:
            year, change = entry.split(':')
            population += int(change) / 1000.0  # Convert change from thousands to millions
        final_population[planet] = round(population, 3)  # Round to three decimal places
    return final_population