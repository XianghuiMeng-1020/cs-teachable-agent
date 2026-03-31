def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile:
            lines = infile.readlines()
            if not lines:
                raise ValueError("No data available")
            total_force = 0
            count = 0
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) != 2:
                    continue
                try:
                    impact_force = float(parts[1])
                    total_force += impact_force
                    count += 1
                except ValueError:
                    continue
            if count == 0:
                raise ValueError("No valid data available")
            average_force = total_force / count
            average_force_str = f'average impact force: {average_force}'
    except (FileNotFoundError, ValueError) as e:
        average_force_str = "No data available"
    with open(output_filename, 'w') as outfile:
        outfile.write(average_force_str)