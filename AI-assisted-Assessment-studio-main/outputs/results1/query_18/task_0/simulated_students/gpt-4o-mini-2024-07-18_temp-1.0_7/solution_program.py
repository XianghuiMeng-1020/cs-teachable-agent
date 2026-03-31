def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}
    with open(input_file, 'r') as f:
        for line in f:
            planet, duration = line.strip().split(',')
            duration = float(duration)
            if planet not in travel_data:
                travel_data[planet] = [0, 0]  # [total_duration, count]
            travel_data[planet][0] += duration
            travel_data[planet][1] += 1

    with open(output_file, 'w') as f:
        for planet, (total_duration, count) in travel_data.items():
            average_duration = total_duration / count
            f.write(f'{planet}:{average_duration:.1f}\n')