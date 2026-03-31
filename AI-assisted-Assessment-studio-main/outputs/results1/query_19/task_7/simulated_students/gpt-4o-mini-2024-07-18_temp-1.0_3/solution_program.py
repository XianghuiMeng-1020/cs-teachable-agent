def analyze_weather(station_id):
    file_name = f'Station{station_id}.txt'
    try:
        with open(file_name, 'r') as file:
            temperatures = []
            for line in file:
                try:
                    temp = float(line.strip())
                    temperatures.append(temp)
                except ValueError:
                    return 'Error: Non-parsable data found in the file.'

            if not temperatures:
                return 'Error: No temperature data available.'

            average_temperature = sum(temperatures) / len(temperatures)
            return average_temperature
    except FileNotFoundError:
        return f'Error: The file {file_name} does not exist.'