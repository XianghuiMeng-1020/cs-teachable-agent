import os

def analyze_weather(station_id):
    file_name = f'Station{station_id}.txt'
    if not os.path.isfile(file_name):
        return 'Error: File not found'
    
    try:
        with open(file_name, 'r') as file:
            temperatures = []
            for line in file:
                try:
                    temperature = float(line.strip())
                    temperatures.append(temperature)
                except ValueError:
                    return 'Error: Non-parsable data found'
        if not temperatures:
            return 'Error: No data available'
        average_temperature = sum(temperatures) / len(temperatures)
        return average_temperature
    except Exception as e:
        return f'Error: {str(e)}'