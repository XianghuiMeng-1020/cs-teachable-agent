def average_energy(file_name):
    if not os.path.exists(file_name):
        return 0
    try:
        with open(file_name, 'r') as file:
            readings = [int(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        return 0
    if len(readings) == 0:
        return 0
    return sum(readings) / len(readings)