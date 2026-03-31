def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}
    with open(input_file, 'r') as f:
        for line in f:
            planet, duration = line.strip().split(',')
            duration = float(duration)
            if planet in travel_data:
                travel_data[planet]['total_duration'] += duration
                travel_data[planet]['count'] += 1
            else:
                travel_data[planet] = {'total_duration': duration, 'count': 1}
    with open(output_file, 'w') as f:
        for planet, data in travel_data.items():
            average_duration = data['total_duration'] / data['count']
            f.write(f'{planet}:{average_duration:.1f}\n')