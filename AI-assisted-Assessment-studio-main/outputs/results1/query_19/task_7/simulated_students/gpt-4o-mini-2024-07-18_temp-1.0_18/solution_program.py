def analyze_weather(station_id):
    filename = f'Station{station_id}.txt'
    try:
        with open(filename, 'r') as file:
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
                return 'Error: No temperature data found.'
            average_temp = total_temp / count
            return average_temp
    except FileNotFoundError:
        return 'Error: File not found.'
    except Exception as e:
        return f'Error: {str(e)}'}