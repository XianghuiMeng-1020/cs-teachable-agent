def process_planet_data(file_name):
    try:
        with open(file_name, 'r') as file:
            habitable_planets = []
            for line in file:
                data = line.strip().split() 
                if len(data) == 3:
                    planet_name = data[0]
                    surface_temp = float(data[2])
                    if -50 <= surface_temp <= 50:
                        habitable_planets.append(planet_name)
            return habitable_planets
    except (FileNotFoundError, IOError):
        return "File Error"
    except ValueError:
        return "File Error"