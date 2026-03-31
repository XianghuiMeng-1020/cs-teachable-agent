def analyze_weather(station_id):
    try:
        filepath = f'Station{station_id}.txt'
        with open(filepath, 'r') as file:
            temperatures = []
            for line in file:
                try:
                    temp = float(line.strip())
                    temperatures.append(temp)
                except ValueError:
                    return 'Error: Non-parsable data encountered in the file.'
            if not temperatures:
                return 'Error: No temperature data found in the file.'
            average_temperature = sum(temperatures) / len(temperatures)
            return average_temperature
    except FileNotFoundError:
        return 'Error: File not found.'
    except Exception as e:
        return f'Error: {str(e)}'