def mythical_creature_stats(input_filename, output_filename):
    creature_data = {}
    with open(input_filename, 'r') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            creature_name, number_of_encounters, distance_traveled = line.split(',')
            number_of_encounters = int(number_of_encounters)
            distance_traveled = float(distance_traveled)
            if creature_name not in creature_data:
                creature_data[creature_name] = [0, 0]  # total encounters and total distance
            creature_data[creature_name][0] += number_of_encounters
            creature_data[creature_name][1] += distance_traveled
    with open(output_filename, 'w') as outfile:
        for creature_name, stats in creature_data.items():
            total_encounters = stats[0]
            total_distance = stats[1]
            average_distance = total_distance / total_encounters if total_encounters > 0 else 0
            outfile.write(f'{creature_name},{total_encounters},{average_distance:.2f}\n')