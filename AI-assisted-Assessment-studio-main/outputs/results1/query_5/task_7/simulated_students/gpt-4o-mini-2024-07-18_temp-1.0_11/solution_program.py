def mythical_creature_stats(input_filename, output_filename):
    from collections import defaultdict
    import csv

    creature_data = defaultdict(lambda: {'encounters': 0, 'distance': 0})

    with open(input_filename, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            creature_name = row[0]
            number_of_encounters = int(row[1])
            distance_traveled = float(row[2])
            creature_data[creature_name]['encounters'] += number_of_encounters
            creature_data[creature_name]['distance'] += distance_traveled

    with open(output_filename, 'w') as outfile:
        for creature, data in creature_data.items():
            total_encounters = data['encounters']
            average_distance = data['distance'] / total_encounters if total_encounters > 0 else 0
            outfile.write(f'{creature},{total_encounters},{average_distance:.2f}\n')
