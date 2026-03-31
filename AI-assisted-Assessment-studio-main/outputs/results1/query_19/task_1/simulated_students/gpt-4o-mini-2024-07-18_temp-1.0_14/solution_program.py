def process_planet_data(file_name):
    try:
        with open(file_name, 'r') as file:
            habitable_planets = []
            for line in file:
                parts = line.strip().split()
                if len(parts) != 3:
                    continue
                planet_name, distance, temperature = parts
                try:
                    temperature = float(temperature)
                    if -50 <= temperature <= 50:
                        habitable_planets.append(planet_name)
                except ValueError:
                    continue
            return habitable_planets
    except (FileNotFoundError, IOError):
        return "File Error"