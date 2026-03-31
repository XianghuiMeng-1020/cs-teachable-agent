def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}
    with open(input_file, 'r') as file:
        for line in file:
            planet, duration = line.strip().split(',')
            duration = float(duration)
            if planet in travel_data:
                travel_data[planet].append(duration)
            else:
                travel_data[planet] = [duration]
    avg_travel = {planet: sum(durations)/len(durations) for planet, durations in travel_data.items()}
    with open(output_file, 'w') as file:
        for planet, avg in avg_travel.items():
            file.write(f'{planet}:{avg:.1f}\n')