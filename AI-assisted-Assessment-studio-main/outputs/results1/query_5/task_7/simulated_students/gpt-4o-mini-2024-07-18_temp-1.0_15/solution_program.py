def mythical_creature_stats(input_filename, output_filename):
    from collections import defaultdict
    import csv

    encounters = defaultdict(lambda: [0, 0])

    with open(input_filename, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            creature = row[0]
            number_of_encounters = int(row[1])
            distance_traveled = float(row[2])
            encounters[creature][0] += number_of_encounters
            encounters[creature][1] += number_of_encounters * distance_traveled

    with open(output_filename, 'w') as outfile:
        for creature, (total_encounters, total_distance) in encounters.items():
            average_distance = total_distance / total_encounters if total_encounters > 0 else 0
            outfile.write(f'{creature},{total_encounters},{average_distance:.2f}\n')