def analyze_weather(station_id):
    filename = f'Station{station_id}.txt'
    try:
        with open(filename, 'r') as file:
            temperatures = file.readlines()
            if not temperatures:
                return 'Error: No temperature data found.'
            temp_values = []
            for line in temperatures:
                try:
                    temp_values.append(float(line.strip()))
                except ValueError:
                    return 'Error: Non-parsable data encountered.'
            if not temp_values:
                return 'Error: No valid temperature data found.'
            average_temp = sum(temp_values) / len(temp_values)
            return average_temp
    except FileNotFoundError:
        return 'Error: File not found.'
    except Exception as e:
        return f'Error: {str(e)}'