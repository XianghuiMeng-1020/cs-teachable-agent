def calculate_total_distance(filename):
    total_distance = 0
    with open(filename, 'r') as file:
        for line in file:
            planet_data = line.split()
            distance = float(planet_data[1])
            total_distance += int(distance)
    return total_distance