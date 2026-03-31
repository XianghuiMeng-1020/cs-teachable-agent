def analyze_data(filename):
    try:
        total_species = 0
        total_population = 0
        with open(filename, 'r') as file:
            for line in file:
                species_info = line.strip().split(',')
                if len(species_info) == 2:
                    species_name = species_info[0].strip()
                    population = int(species_info[1].strip())
                    total_species += 1
                    total_population += population
        return (total_species, total_population)
    except:
        return (0, 0)