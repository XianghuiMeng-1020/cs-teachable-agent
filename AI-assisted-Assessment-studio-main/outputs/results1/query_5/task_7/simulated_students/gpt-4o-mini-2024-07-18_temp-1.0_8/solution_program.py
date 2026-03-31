def mythical_creature_stats(input_filename, output_filename):
    encounter_data = {}

    with open(input_filename, 'r') as infile:
        for line in infile:
            parts = line.strip().split(',')
            creature = parts[0]
            encounters = int(parts[1])
            distance = float(parts[2])

            if creature not in encounter_data:
                encounter_data[creature] = {'total_encounters': 0, 'total_distance': 0.0}

            encounter_data[creature]['total_encounters'] += encounters
            encounter_data[creature]['total_distance'] += distance

    with open(output_filename, 'w') as outfile:
        for creature, stats in encounter_data.items():
            total_encounters = stats['total_encounters']
            average_distance = stats['total_distance'] / total_encounters if total_encounters > 0 else 0
            outfile.write(f"{creature},{total_encounters},{average_distance:.2f}\n")