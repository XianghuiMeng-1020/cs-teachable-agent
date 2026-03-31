def analyze_weather(station_id):
    filename = f'Station{station_id}.txt'
    try:
        with open(filename, 'r') as file:
            temperatures = []
            for line in file:
                try:
                    temp = float(line.strip())
                    temperatures.append(temp)
                except ValueError:
                    return 'Error: Non-parsable data found.'
            if not temperatures:
                return 'Error: No temperature data found.'
            average_temp = sum(temperatures) / len(temperatures)
            return average_temp
    except FileNotFoundError:
        return 'Error: File not found.'
    except Exception as e:
        return f'Error: {str(e)}'