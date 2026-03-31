def process_planet_data(file_name):
    try:
        with open(file_name, 'r') as file:
            habitable_planets = []
            for line in file:
                parts = line.strip().split()  
                if len(parts) < 3:
                    continue  
                planet_name = parts[0]
                try:
                    surface_temp = float(parts[2])
                except ValueError:
                    continue
                if -50 <= surface_temp <= 50:
                    habitable_planets.append(planet_name)
            return habitable_planets
    except (FileNotFoundError, IOError):
        return "File Error"