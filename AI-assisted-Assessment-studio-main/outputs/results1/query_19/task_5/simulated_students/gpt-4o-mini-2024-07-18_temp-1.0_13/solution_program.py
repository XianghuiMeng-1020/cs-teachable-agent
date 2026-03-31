def analyze_data(filename):
    try:
        total_species = 0
        total_population = 0
        with open(filename, 'r') as file:
            for line in file:
                species_data = line.strip().split(',')
                if len(species_data) == 2:
                    total_species += 1
                    total_population += int(species_data[1].strip())
        return (total_species, total_population)
    except:
        return (0, 0)