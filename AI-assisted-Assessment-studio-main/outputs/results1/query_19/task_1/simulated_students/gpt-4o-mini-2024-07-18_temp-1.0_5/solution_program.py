def process_planet_data(file_name):
    try:
        with open(file_name, 'r') as file:
            results = []
            for line in file:
                parts = line.strip().split()  
                if len(parts) == 3:
                    planet_name = parts[0]
                    try:
                        surface_temp = float(parts[2])
                        if -50 <= surface_temp <= 50:
                            results.append(planet_name)
                    except ValueError:
                        continue
            return results
    except Exception:
        return "File Error"