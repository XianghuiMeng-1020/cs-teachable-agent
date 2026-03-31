def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            planet, duration = line.strip().split(',')
            duration = float(duration)
            if planet not in travel_data:
                travel_data[planet] = []
            travel_data[planet].append(duration)

    avg_travel_times = {}
    for planet, durations in travel_data.items():
        avg_travel_times[planet] = round(sum(durations) / len(durations), 1)

    with open(output_file, 'w') as outfile:
        for planet, avg_duration in avg_travel_times.items():
            outfile.write(f'{planet}:{avg_duration}\n')