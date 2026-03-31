def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}
    journeys_count = {}

    with open(input_file, 'r') as file:
        for line in file:
            planet, duration = line.strip().split(',')
            duration = float(duration)

            if planet in travel_data:
                travel_data[planet] += duration
                journeys_count[planet] += 1
            else:
                travel_data[planet] = duration
                journeys_count[planet] = 1

    with open(output_file, 'w') as file:
        for planet, total_duration in travel_data.items():
            avg_duration = total_duration / journeys_count[planet]
            file.write(f'{planet}:{avg_duration:.1f}\n')