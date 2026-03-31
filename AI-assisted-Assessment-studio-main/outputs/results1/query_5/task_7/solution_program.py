def mythical_creature_stats(input_filename, output_filename):
    creature_data = {}
    with open(input_filename, 'r') as file:
        for line in file:
            name, encounters, distance = line.strip().split(',')
            encounters = int(encounters)
            distance = int(distance)
            if name in creature_data:
                creature_data[name]['total_encounters'] += encounters
                creature_data[name]['total_distance'] += distance
            else:
                creature_data[name] = {'total_encounters': encounters, 'total_distance': distance}
    with open(output_filename, 'w') as file:
        for name, data in creature_data.items():
            total_encounters = data['total_encounters']
            average_distance = round(data['total_distance'] / total_encounters, 2)
            file.write(f"{name},{total_encounters},{average_distance:.2f}\n")