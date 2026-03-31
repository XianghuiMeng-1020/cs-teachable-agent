def analyze_weather(station_id):
    try:
        file_name = f'Station{station_id}.txt'
        with open(file_name, 'r') as file:
            temperatures = file.readlines()
            total_temp = 0.0
            count = 0
            for line in temperatures:
                try:
                    temp = float(line.strip())
                    total_temp += temp
                    count += 1
                except ValueError:
                    return 'Error: Non-parsable data found in the file.'
            if count == 0:
                return 'Error: No temperature data found in the file.'
            average_temp = total_temp / count
            return average_temp
    except FileNotFoundError:
        return 'Error: Weather data file not found.'