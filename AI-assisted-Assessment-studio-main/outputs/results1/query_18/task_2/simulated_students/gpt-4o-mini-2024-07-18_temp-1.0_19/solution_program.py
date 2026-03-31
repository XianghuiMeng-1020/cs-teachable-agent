def average_energy(file_name):
    try:
        with open(file_name, 'r') as file:
            readings = [int(line.strip()) for line in file if line.strip()]
            if not readings:
                return 0
            return sum(readings) / len(readings)
    except (FileNotFoundError, ValueError):
        return 0