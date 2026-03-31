def alien_population_change(data):
    result = {}
    for planet, changes in data.items():
        population = 1.0  # Starting at 1 million
        for change in changes:
            year, change_amount = change.split(':')
            population += float(change_amount) / 1000.0  # Convert to millions
        result[planet] = round(population, 3)
    return result