def analyze_weather(station_id):
    filename = f'Station{station_id}.txt'
    try:
        with open(filename, 'r') as file:
            temperatures = file.readlines()
        if not temperatures:
            return 'Error: No data available'
        total_temp = 0
        count = 0
        for temp in temperatures:
            try:
                total_temp += float(temp.strip())
                count += 1
            except ValueError:
                return 'Error: Non-parsable data encountered'
        if count == 0:
            return 'Error: No valid data to compute average'
        average_temp = total_temp / count
        return average_temp
    except FileNotFoundError:
        return 'Error: File not found'
    except Exception as e:
        return f'Error: {str(e)}'