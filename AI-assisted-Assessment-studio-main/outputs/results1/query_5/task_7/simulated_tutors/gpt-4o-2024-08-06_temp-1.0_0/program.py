def mythical_creature_stats(input_filename, output_filename):
    creature_data = {}

    # Reading from the input file
    with open(input_filename, 'r') as file:
        for line in file:
            creature_name, encounters, distance = line.strip().split(',')
            encounters = int(encounters)
            distance = int(distance)

            # Check if the creature is already in the dictionary
            if creature_name in creature_data:
                creature_data[creature_name]['total_encounters'] += encounters
                creature_data[creature_name]['total_distance'] += distance
            else:
                creature_data[creature_name] = {
                    'total_encounters': encounters,
                    'total_distance': distance
                }

    # Writing to the output file
    with open(output_filename, 'w') as file:
        for creature_name, data in creature_data.items():
            total_encounters = data['total_encounters']
            total_distance = data['total_distance']
            average_distance = round(total_distance / total_encounters, 2)
            file.write(f"{creature_name},{total_encounters},{average_distance:.2f}\n")