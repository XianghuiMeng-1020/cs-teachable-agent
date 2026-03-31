def mythical_creature_stats(input_filename, output_filename):
    from collections import defaultdict
    import os

    if not os.path.exists(input_filename):
        return

    creatures = defaultdict(lambda: [0, 0.0])

    with open(input_filename, 'r') as infile:
        for line in infile:
            creature_name, encounters, distance = line.strip().split(',')
            encounters = int(encounters)
            distance = float(distance)
            creatures[creature_name][0] += encounters
            creatures[creature_name][1] += distance

    with open(output_filename, 'w') as outfile:
        for creature_name, (total_encounters, total_distance) in creatures.items():
            average_distance = total_distance / total_encounters if total_encounters > 0 else 0
            outfile.write(f'{creature_name},{total_encounters},{average_distance:.2f}\n')