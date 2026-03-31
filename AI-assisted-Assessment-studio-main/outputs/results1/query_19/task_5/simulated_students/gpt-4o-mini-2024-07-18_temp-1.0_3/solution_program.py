def analyze_data(filename):
    total_species = 0
    total_population = 0
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    species = parts[0]
                    population = int(parts[1])
                    total_species += 1
                    total_population += population
    except (FileNotFoundError, IOError, ValueError):
        return (0, 0)
    return (total_species, total_population)