def alien_population_change(data):
    result = {}
    for planet, changes in data.items():
        population = 1.0
        for change in changes:
            _, change_value = change.split(':')
            population += int(change_value) / 1000.0
        result[planet] = round(population, 3)
    return result