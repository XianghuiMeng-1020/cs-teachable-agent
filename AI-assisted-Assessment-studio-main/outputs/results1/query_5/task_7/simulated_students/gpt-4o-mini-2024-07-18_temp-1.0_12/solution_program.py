def mythical_creature_stats(input_filename, output_filename):
    creature_data = {}

    with open(input_filename, 'r') as infile:
        for line in infile:
            parts = line.strip().split(',')
            creature_name = parts[0]
            number_of_encounters = int(parts[1])
            distance_traveled = float(parts[2])

            if creature_name not in creature_data:
                creature_data[creature_name] = {'total_encounters': 0, 'total_distance': 0.0}
            creature_data[creature_name]['total_encounters'] += number_of_encounters
            creature_data[creature_name]['total_distance'] += distance_traveled

    with open(output_filename, 'w') as outfile:
        for creature_name, data in creature_data.items():
            total_encounters = data['total_encounters']
            average_distance = data['total_distance'] / total_encounters
            outfile.write(f'{creature_name},{total_encounters},{average_distance:.2f}\n')