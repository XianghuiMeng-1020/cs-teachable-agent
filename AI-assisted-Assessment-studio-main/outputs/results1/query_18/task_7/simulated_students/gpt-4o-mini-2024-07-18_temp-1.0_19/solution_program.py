def calculate_total_distance(filename):
    total_distance = 0
    with open(filename, 'r') as file:
        for line in file:
            planet_data = line.split()  # Split line into parts
            distance = float(planet_data[1])  # Get the distance part
            total_distance += int(distance)  # Add distance as an integer
    return total_distance