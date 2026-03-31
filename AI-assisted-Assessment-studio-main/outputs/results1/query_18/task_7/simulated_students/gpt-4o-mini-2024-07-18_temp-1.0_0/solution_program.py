def calculate_total_distance(filename):
    total_distance = 0
    with open(filename, 'r') as file:
        for line in file:
            _, distance = line.strip().split()
            total_distance += int(float(distance))
    return total_distance