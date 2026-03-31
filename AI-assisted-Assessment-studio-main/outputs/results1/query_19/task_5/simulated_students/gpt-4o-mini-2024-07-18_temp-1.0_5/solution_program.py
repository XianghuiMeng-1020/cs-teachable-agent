def analyze_data(filename):
    try:
        total_species = 0
        total_population = 0
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    species = parts[0].strip()
                    population = int(parts[1].strip())
                    total_species += 1
                    total_population += population
        return (total_species, total_population)
    except:
        return (0, 0)