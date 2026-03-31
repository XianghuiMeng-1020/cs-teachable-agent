def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            planet, duration = line.strip().split(',')
            duration = float(duration)
            if planet not in travel_data:
                travel_data[planet] = []
            travel_data[planet].append(duration)

    with open(output_file, 'w') as outfile:
        for planet, durations in travel_data.items():
            avg_duration = sum(durations) / len(durations)
            outfile.write(f'{planet}:{avg_duration:.1f}\n')