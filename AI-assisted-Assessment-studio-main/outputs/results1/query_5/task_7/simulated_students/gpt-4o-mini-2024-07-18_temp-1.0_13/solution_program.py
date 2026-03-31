def mythical_creature_stats(input_filename, output_filename):
    encounters = {}
    total_distance = {}

    with open(input_filename, 'r') as infile:
        for line in infile:
            creature, num_encounters, distance_traveled = line.strip().split(',')
            num_encounters = int(num_encounters)
            distance_traveled = float(distance_traveled)

            if creature not in encounters:
                encounters[creature] = 0
                total_distance[creature] = 0.0

            encounters[creature] += num_encounters
            total_distance[creature] += distance_traveled

    with open(output_filename, 'w') as outfile:
        for creature in encounters:
            total_encounters = encounters[creature]
            average_distance = total_distance[creature] / total_encounters
            outfile.write(f'{creature},{total_encounters},{average_distance:.2f}\n')