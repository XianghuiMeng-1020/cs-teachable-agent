def analyze_data(filename):
    try:
        with open(filename, 'r') as file:
            total_species = 0
            total_population = 0
            for line in file:
                species, population = line.strip().split(',')
                total_species += 1
                total_population += int(population)
            return (total_species, total_population)
    except (FileNotFoundError, IOError, ValueError):
        return (0, 0)