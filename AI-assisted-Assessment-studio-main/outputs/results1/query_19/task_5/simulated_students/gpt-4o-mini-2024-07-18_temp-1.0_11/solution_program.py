def analyze_data(filename):
    try:
        with open(filename, 'r') as file:
            total_population = 0
            total_species = 0
            for line in file:
                if line.strip():
                    species_data = line.split(',')
                    species_name = species_data[0].strip()
                    population = int(species_data[1].strip())
                    total_species += 1
                    total_population += population
            return (total_species, total_population)
    except (FileNotFoundError, IOError, ValueError):
        return (0, 0)