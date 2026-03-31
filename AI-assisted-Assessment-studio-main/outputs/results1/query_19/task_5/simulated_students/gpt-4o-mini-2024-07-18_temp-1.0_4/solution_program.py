def analyze_data(filename):
    try:
        with open(filename, 'r') as file:
            total_species = 0
            total_population = 0
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    species_name = parts[0]
                    population = int(parts[1])
                    total_species += 1
                    total_population += population
        return (total_species, total_population)
    except (FileNotFoundError, IOError, ValueError):
        return (0, 0)