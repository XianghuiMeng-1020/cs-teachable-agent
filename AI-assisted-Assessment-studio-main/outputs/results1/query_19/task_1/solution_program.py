def process_planet_data(file_name):
    habitable_planets = []
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                try:
                    name, distance, temperature = line.strip().split()
                    temperature = float(temperature)
                    if -50 <= temperature <= 50:
                        habitable_planets.append(name)
                except ValueError:
                    return "File Error"
    except (FileNotFoundError, IOError):
        return "File Error"
    return habitable_planets
