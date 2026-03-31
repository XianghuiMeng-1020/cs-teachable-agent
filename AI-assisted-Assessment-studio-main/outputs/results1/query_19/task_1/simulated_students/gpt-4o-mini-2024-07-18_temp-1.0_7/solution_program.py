def process_planet_data(file_name):
    try:
        with open(file_name, 'r') as file:
            habitable_planets = []
            for line in file:
                data = line.strip().split()  # Split the line into its components
                if len(data) != 3:
                    continue  # Skip lines that don't have exactly 3 components
                planet_name = data[0]
                try:
                    surface_temp = float(data[2])
                    if -50 <= surface_temp <= 50:
                        habitable_planets.append(planet_name)
                except ValueError:
                    continue  # Handle cases where surface temperature isn't a number
            return habitable_planets
    except (FileNotFoundError, IOError):
        return 'File Error'