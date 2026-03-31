def alien_population_change(data):
    result = {}
    for planet, changes in data.items():
        population = 1000
        for record in changes:
            year, change = record.split(':')
            population += int(change)
        result[planet] = population / 1000
    return result