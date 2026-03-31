def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}
    counts = {}

    with open(input_file, 'r') as file:
        for line in file:
            planet, duration = line.strip().split(',')
            duration = float(duration)
            if planet in travel_data:
                travel_data[planet] += duration
                counts[planet] += 1
            else:
                travel_data[planet] = duration
                counts[planet] = 1

    with open(output_file, 'w') as file:
        for planet in travel_data:
            average_duration = travel_data[planet] / counts[planet]
            file.write(f'{planet}:{average_duration:.1f}\n')