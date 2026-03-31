def alien_population_change(data):
    result = {}
    for planet, changes in data.items():
        population = 1.0  # start with 1 million
        for change in changes:
            _, change_value = change.split(':')
            population += int(change_value) / 1000.0  # convert to millions
        result[planet] = round(population, 3)
    return result