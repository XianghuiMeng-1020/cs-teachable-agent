def calculate_avg_travel_time(input_file, output_file):
    travel_data = {}
    
    # Read input file
    with open(input_file, 'r') as file:
        for line in file:
            planet, duration = line.strip().split(",")
            duration = float(duration)
            
            if planet in travel_data:
                travel_data[planet]['total_duration'] += duration
                travel_data[planet]['count'] += 1
            else:
                travel_data[planet] = {'total_duration': duration, 'count': 1}
    
    # Calculate average duration for each planet
    avg_durations = {}
    for planet, data in travel_data.items():
        avg_duration = round(data['total_duration'] / data['count'], 1)
        avg_durations[planet] = avg_duration
    
    # Write results to the output file
    with open(output_file, 'w') as file:
        for planet, avg_duration in avg_durations.items():
            file.write(f"{planet}:{avg_duration}\n")