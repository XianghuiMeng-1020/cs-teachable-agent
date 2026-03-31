def average_energy(file_name):
    try:
        with open(file_name, 'r') as file:
            readings = file.readlines()
            if not readings:
                return 0
            total = sum(int(line.strip()) for line in readings)
            count = len(readings)
            return total / count
    except (FileNotFoundError, ValueError):
        return 0