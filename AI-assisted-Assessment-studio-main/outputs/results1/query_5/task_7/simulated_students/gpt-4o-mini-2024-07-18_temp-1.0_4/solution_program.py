def mythical_creature_stats(input_filename, output_filename):
    creature_data = {}

    with open(input_filename, 'r') as infile:
        for line in infile:
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue
            creature_name = parts[0].strip()
            number_of_encounters = int(parts[1].strip())
            distance_traveled = float(parts[2].strip())

            if creature_name not in creature_data:
                creature_data[creature_name] = [0, 0]  # [total_encounters, total_distance]

            creature_data[creature_name][0] += number_of_encounters
            creature_data[creature_name][1] += distance_traveled

    with open(output_filename, 'w') as outfile:
        for creature_name, data in creature_data.items():
            total_encounters = data[0]
            average_distance = data[1] / total_encounters if total_encounters > 0 else 0
            outfile.write(f'{creature_name},{total_encounters},{average_distance:.2f}\n')