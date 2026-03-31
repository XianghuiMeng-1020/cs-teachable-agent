def mythical_creature_stats(input_filename, output_filename):
    creature_data = {}
    
    with open(input_filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            creature_name = parts[0]
            number_of_encounters = int(parts[1])
            distance_traveled = float(parts[2])
            
            if creature_name not in creature_data:
                creature_data[creature_name] = {'total_encounters': 0, 'total_distance': 0.0}
            
            creature_data[creature_name]['total_encounters'] += number_of_encounters
            creature_data[creature_name]['total_distance'] += distance_traveled
    
    with open(output_filename, 'w') as output_file:
        for creature, data in creature_data.items():
            total_encounters = data['total_encounters']
            average_distance = data['total_distance'] / total_encounters
            output_file.write(f"{creature},{total_encounters},{average_distance:.2f}\n")