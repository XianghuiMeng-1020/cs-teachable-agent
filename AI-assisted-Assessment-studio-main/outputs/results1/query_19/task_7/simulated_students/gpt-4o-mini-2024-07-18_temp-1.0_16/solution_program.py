def analyze_weather(station_id):
    filename = f'Station{station_id}.txt'
    try:
        with open(filename, 'r') as file:
            temperatures = []
            for line in file:
                try:
                    temperature = float(line.strip())
                    temperatures.append(temperature)
                except ValueError:
                    return f'Error: Non-parsable data found in {filename}'
        if not temperatures:
            return f'Error: No data found in {filename}'
        average_temp = sum(temperatures) / len(temperatures)
        return average_temp
    except FileNotFoundError:
        return f'Error: File {filename} not found'
    except Exception as e:
        return f'Error: {str(e)}'