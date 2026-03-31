def calculate_total_distance(filename):
    total_distance = 0
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            distance = float(parts[1])
            total_distance += int(distance)
    return total_distance