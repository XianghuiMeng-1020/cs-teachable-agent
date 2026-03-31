def mythical_creature_stats(input_filename, output_filename):
    creature_data = {}

    with open(input_filename, 'r') as infile:
        for line in infile:
            creature_name, encounters, distance = line.strip().split(',')
            encounters = int(encounters)
            distance = float(distance)

            if creature_name not in creature_data:
                creature_data[creature_name] = {'total_encounters': 0, 'total_distance': 0.0}

            creature_data[creature_name]['total_encounters'] += encounters
            creature_data[creature_name]['total_distance'] += distance * encounters

    with open(output_filename, 'w') as outfile:
        for creature_name, stats in creature_data.items():
            total_encounters = stats['total_encounters']
            average_distance = stats['total_distance'] / total_encounters if total_encounters > 0 else 0
            outfile.write(f'{creature_name},{total_encounters},{average_distance:.2f}\n')