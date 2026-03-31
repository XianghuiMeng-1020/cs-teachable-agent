def analyze_data(filename):
    try:
        with open(filename, 'r') as file:
            total_species = 0
            total_population = 0
            for line in file:
                species_info = line.strip().split(',')
                if len(species_info) == 2:
                    total_species += 1
                    total_population += int(species_info[1].strip())
            return (total_species, total_population)
    except (FileNotFoundError, IOError):
        return (0, 0)