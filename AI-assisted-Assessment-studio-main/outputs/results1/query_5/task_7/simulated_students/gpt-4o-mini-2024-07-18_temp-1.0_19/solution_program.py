def mythical_creature_stats(input_filename, output_filename):
    creature_data = {}
    with open(input_filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            creature_name = parts[0]
            number_of_encounters = int(parts[1])
            distance_traveled = float(parts[2])
            if creature_name not in creature_data:
                creature_data[creature_name] = [0, 0.0]  # [total encounters, total distance]
            creature_data[creature_name][0] += number_of_encounters
            creature_data[creature_name][1] += distance_traveled

    with open(output_filename, 'w') as file:
        for creature, data in creature_data.items():
            total_encounters = data[0]
            average_distance = data[1] / total_encounters if total_encounters > 0 else 0
            file.write(f'{creature},{total_encounters},{average_distance:.2f}\n')