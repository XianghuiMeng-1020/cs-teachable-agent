def analyze_data(filename):
    total_species = 0
    total_population = 0
    try:
        with open(filename, 'r') as file:
            for line in file:
                species, population = line.strip().split(',')
                total_species += 1
                total_population += int(population)
    except (FileNotFoundError, IOError, ValueError):
        return (0, 0)
    return (total_species, total_population)