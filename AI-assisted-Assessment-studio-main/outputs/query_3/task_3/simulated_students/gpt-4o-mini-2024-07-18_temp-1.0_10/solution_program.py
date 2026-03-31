def alien_population_change(data):
    result = {}
    for planet, changes in data.items():
        population = 1.0  # Starting population in millions
        for change in changes:
            year, change_value = change.split(':')
            population += float(change_value) / 1000.0  # Convert thousands to millions
        result[planet] = round(population, 3)  # Round to three decimal places
    return result