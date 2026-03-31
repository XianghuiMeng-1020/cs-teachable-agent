def analyze_weather(station_id):
    try:
        filename = f'Station{station_id}.txt'
        with open(filename, 'r') as file:
            temperatures = []
            for line in file:
                try:
                    temp = float(line.strip())
                    temperatures.append(temp)
                except ValueError:
                    return 'Error: Non-parsable data encountered.'
            if not temperatures:
                return 'Error: No temperature data found in the file.'
            average_temp = sum(temperatures) / len(temperatures)
            return average_temp
    except FileNotFoundError:
        return 'Error: The specified file does not exist.'