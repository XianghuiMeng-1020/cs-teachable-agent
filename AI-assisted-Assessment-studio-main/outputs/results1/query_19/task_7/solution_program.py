def analyze_weather(station_id):
    filename = f'Station{station_id}.txt'
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            temperatures = []
            for line in lines:
                try:
                    temp = float(line.strip())
                    temperatures.append(temp)
                except ValueError:
                    raise ValueError("Non-parsable data encountered.")
            if not temperatures:
                return 'Error: No valid temperature data found.'
            average_temp = sum(temperatures) / len(temperatures)
            return round(average_temp, 2)
    except FileNotFoundError:
        return "Error: File not found."
    except ValueError as e:
        return f"Error: {str(e)}"