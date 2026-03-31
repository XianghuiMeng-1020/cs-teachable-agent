def process_planet_data(file_name):
    habitable_planets = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                try:
                    # Splitting the line into parts
                    parts = line.strip().split()
                    if len(parts) != 3:
                        return "File Error"

                    planet_name = parts[0]
                    distance = float(parts[1])  # It might be useful in more advanced tasks
                    temperature = float(parts[2])

                    # Check if planet is habitable
                    if -50 <= temperature <= 50:
                        habitable_planets.append(planet_name)
                except ValueError:
                    return "File Error"
    except (FileNotFoundError, IOError):
        return "File Error"

    return habitable_planets