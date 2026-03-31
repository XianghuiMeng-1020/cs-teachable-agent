def calculate_avg_travel_time(input_file, output_file):
    planet_time = {}
    with open(input_file, 'r') as f:
        for line in f:
            planet, time = line.strip().split(',')
            if planet in planet_time:
                planet_time[planet].append(float(time))
            else:
                planet_time[planet] = [float(time)]
    with open(output_file, 'w') as f:
        for planet in planet_time:
            avg_time = sum(planet_time[planet]) / len(planet_time[planet])
            f.write(f"{planet}:{avg_time:.1f}\n")