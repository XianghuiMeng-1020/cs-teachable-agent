def alien_population_change(data):
    result = {}
    for planet, changes in data.items():
        current_population = 1.0  # Starting at 1 million
        for entry in changes:
            year, change = entry.split(':')
            current_population += int(change) / 1000  # Convert change to millions
        result[planet] = round(current_population, 3)  # Round to 3 decimal places
    return result