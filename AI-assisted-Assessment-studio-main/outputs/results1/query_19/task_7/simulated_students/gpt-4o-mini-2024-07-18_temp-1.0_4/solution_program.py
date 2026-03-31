def analyze_weather(station_id):
    file_name = f'Station{station_id}.txt'
    try:
        with open(file_name, 'r') as file:
            temperatures = []
            for line in file:
                try:
                    temperature = float(line.strip())
                    temperatures.append(temperature)
                except ValueError:
                    return 'Error: Non-parsable data found in the file.'
        if not temperatures:
            return 'Error: No data found in the file.'
        average_temperature = sum(temperatures) / len(temperatures)
        return average_temperature
    except FileNotFoundError:
        return 'Error: Weather data file not found.'
    except Exception as e:
        return f'Error: {str(e)}'