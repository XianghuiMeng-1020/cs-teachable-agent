def analyze_data(filename):
    try:
        total_species = 0
        total_population = 0
        with open(filename, 'r') as file:
            for line in file:
                total_species += 1
                species_data = line.strip().split(',')
                if len(species_data) == 2:
                    population = int(species_data[1].strip())
                    total_population += population
        return (total_species, total_population)
    except:
        return (0, 0)