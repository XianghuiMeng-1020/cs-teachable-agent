def mythical_creature_stats(input_filename, output_filename):
    encounters = {}  
    with open(input_filename, 'r') as infile:
        for line in infile:
            parts = line.strip().split(',')  
            creature = parts[0]  
            number_of_encounters = int(parts[1])  
            distance_traveled = float(parts[2])  
            if creature not in encounters:
                encounters[creature] = {'total_encounters': 0, 'total_distance': 0}
            encounters[creature]['total_encounters'] += number_of_encounters
            encounters[creature]['total_distance'] += distance_traveled
    with open(output_filename, 'w') as outfile:
        for creature, stats in encounters.items():
            average_distance = stats['total_distance'] / stats['total_encounters']
            outfile.write(f'{creature},{stats["total_encounters"]},{average_distance:.2f}\n')