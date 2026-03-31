def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}

    with open(input_file, 'r') as f:
        for line in f:
            planet, duration = line.strip().split(',')
            duration = float(duration)
            if planet in travel_data:
                travel_data[planet].append(duration)
            else:
                travel_data[planet] = [duration]

    with open(output_file, 'w') as f:
        for planet, durations in travel_data.items():
            avg_duration = sum(durations) / len(durations)
            f.write(f'{planet}:{avg_duration:.1f}\n')