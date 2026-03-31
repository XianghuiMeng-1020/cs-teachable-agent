def process_planet_data(file_name):
    try:
        with open(file_name, 'r') as file:
            habitable_planets = []
            for line in file:
                data = line.strip().split()
                if len(data) != 3:
                    continue
                planet_name, distance, temperature = data
                temperature = float(temperature)
                if -50 <= temperature <= 50:
                    habitable_planets.append(planet_name)
            return habitable_planets
    except Exception:
        return "File Error"