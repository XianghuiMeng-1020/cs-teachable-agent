def analyze_data(filename):
    try:
        total_species = 0
        total_population = 0
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    species, population = line.split(',')
                    total_species += 1
                    total_population += int(population)
        return (total_species, total_population)
    except Exception:
        return (0, 0)