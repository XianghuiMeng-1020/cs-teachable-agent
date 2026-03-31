def mythical_creature_stats(input_filename, output_filename):
    creature_stats = {}
    
    with open(input_filename, 'r') as infile:
        for line in infile:
            parts = line.strip().split(',')
            creature_name = parts[0]
            number_of_encounters = int(parts[1])
            distance_traveled = float(parts[2])
            
            if creature_name in creature_stats:
                creature_stats[creature_name]['total_encounters'] += number_of_encounters
                creature_stats[creature_name]['total_distance'] += distance_traveled
            else:
                creature_stats[creature_name] = {
                    'total_encounters': number_of_encounters,
                    'total_distance': distance_traveled
                }
    
    with open(output_filename, 'w') as outfile:
        for creature, stats in creature_stats.items():
            total_encounters = stats['total_encounters']
            average_distance = stats['total_distance'] / total_encounters
            outfile.write(f'{creature},{total_encounters},{average_distance:.2f}\n')