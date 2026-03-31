def mythical_creature_stats(input_filename, output_filename):
    from collections import defaultdict
    
    encounters = defaultdict(lambda: {'total_encounters': 0, 'total_distance': 0})
    
    with open(input_filename, 'r') as infile:
        for line in infile:
            parts = line.strip().split(',')
            creature_name = parts[0].strip()
            number_of_encounters = int(parts[1].strip())
            distance_traveled = float(parts[2].strip())
            
            encounters[creature_name]['total_encounters'] += number_of_encounters
            encounters[creature_name]['total_distance'] += distance_traveled
    
    with open(output_filename, 'w') as outfile:
        for creature, data in encounters.items():
            total_encounters = data['total_encounters']
            average_distance = data['total_distance'] / total_encounters if total_encounters > 0 else 0
            outfile.write(f"{creature},{total_encounters},{average_distance:.2f}\n")