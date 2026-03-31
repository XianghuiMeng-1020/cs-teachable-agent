def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}
    journey_counts = {}

    with open(input_file, 'r') as file:
        for line in file:
            planet_name, duration = line.strip().split(',')
            duration = float(duration)
            if planet_name in travel_data:
                travel_data[planet_name] += duration
                journey_counts[planet_name] += 1
            else:
                travel_data[planet_name] = duration
                journey_counts[planet_name] = 1

    with open(output_file, 'w') as file:
        for planet_name in travel_data:
            average_duration = travel_data[planet_name] / journey_counts[planet_name]
            file.write(f'{planet_name}:{average_duration:.1f}\n')