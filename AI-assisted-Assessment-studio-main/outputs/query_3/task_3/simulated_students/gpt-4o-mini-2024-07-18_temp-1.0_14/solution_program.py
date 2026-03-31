def alien_population_change(data):
    results = {}
    for planet, changes in data.items():
        population = 1.0  # starting population in millions
        for change in changes:
            year, change_value = change.split(':')
            population += float(change_value) / 1000  # convert change to millions
        results[planet] = round(population, 3)  # round to 3 decimal places
    return results