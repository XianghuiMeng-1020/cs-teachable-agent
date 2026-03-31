def alien_population_change(data):
    result = {}
    for planet, changes in data.items():
        population = 1.0  # starting population in millions
        for change in changes:
            year, pop_change = change.split(':')
            population += float(pop_change) / 1000  # convert thousands to millions
        result[planet] = round(population, 3)  # rounding to three decimal places
    return result