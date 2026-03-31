def analyze_data(filename):
    total_species = 0
    total_population = 0
    try:
        with open(filename, 'r') as file:
            for line in file:
                species_data = line.strip().split(',')
                if len(species_data) == 2:
                    species_name, population = species_data
                    total_species += 1
                    total_population += int(population)
    except (FileNotFoundError, IOError):
        return (0, 0)
    return (total_species, total_population)