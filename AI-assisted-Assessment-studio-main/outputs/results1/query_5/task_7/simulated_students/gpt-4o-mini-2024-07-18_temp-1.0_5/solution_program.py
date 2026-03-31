def mythical_creature_stats(input_filename, output_filename):
    creature_data = {}

    with open(input_filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(',')
                creature_name = parts[0]
                number_of_encounters = int(parts[1])
                distance_traveled = float(parts[2])

                if creature_name not in creature_data:
                    creature_data[creature_name] = [0, 0.0]  # total encounters, total distance

                creature_data[creature_name][0] += number_of_encounters
                creature_data[creature_name][1] += distance_traveled

    with open(output_filename, 'w') as file:
        for creature_name, stats in creature_data.items():
            total_encounters = stats[0]
            total_distance = stats[1]
            average_distance = total_distance / total_encounters if total_encounters > 0 else 0.0
            file.write(f'{creature_name},{total_encounters},{average_distance:.2f}\n')