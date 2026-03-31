def average_energy(file_name):
    try:
        with open(file_name, 'r') as file:
            readings = file.readlines()
            if not readings:
                return 0
            total = sum(int(reading.strip()) for reading in readings)
            average = total / len(readings)
            return average
    except (FileNotFoundError, ValueError):
        return 0