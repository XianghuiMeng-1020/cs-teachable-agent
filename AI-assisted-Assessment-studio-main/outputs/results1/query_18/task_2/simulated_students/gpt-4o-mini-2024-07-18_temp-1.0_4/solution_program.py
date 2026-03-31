def average_energy(file_name):
    try:
        with open(file_name, 'r') as file:
            readings = [int(line.strip()) for line in file.readlines()]
        if readings:
            return sum(readings) / len(readings)
        else:
            return 0
    except (FileNotFoundError, ValueError):
        return 0