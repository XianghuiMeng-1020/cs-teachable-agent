def mythical_creature_stats(input_filename, output_filename):
    from collections import defaultdict
    import csv

    creature_data = defaultdict(lambda: {'total_encounters': 0, 'total_distance': 0.0})

    with open(input_filename, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            creature_name = row[0]
            number_of_encounters = int(row[1])
            distance_traveled = float(row[2])

            creature_data[creature_name]['total_encounters'] += number_of_encounters
            creature_data[creature_name]['total_distance'] += distance_traveled

    with open(output_filename, 'w') as outfile:
        writer = csv.writer(outfile)
        for creature_name, stats in creature_data.items():
            total_encounters = stats['total_encounters']
            average_distance = stats['total_distance'] / total_encounters if total_encounters > 0 else 0.0
            writer.writerow([creature_name, total_encounters, round(average_distance, 2)])