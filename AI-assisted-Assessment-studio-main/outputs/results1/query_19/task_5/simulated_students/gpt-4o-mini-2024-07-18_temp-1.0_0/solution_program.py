def analyze_data(filename):
    total_species = 0
    total_population = 0
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    species, population = line.split(',')
                    total_species += 1
                    total_population += int(population.strip())
    except (FileNotFoundError, IOError, ValueError):
        return (0, 0)
    return (total_species, total_population)