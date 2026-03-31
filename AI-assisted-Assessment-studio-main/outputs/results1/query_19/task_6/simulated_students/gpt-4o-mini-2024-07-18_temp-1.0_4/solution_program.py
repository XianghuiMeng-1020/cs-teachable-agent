def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as input_file:
            lines = input_file.readlines()
            if not lines:
                raise ValueError('No data in file')
            total_force = 0
            count = 0
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) < 2:
                    continue
                impact_force = float(parts[1])
                total_force += impact_force
                count += 1
            if count == 0:
                raise ValueError('No valid data')
            average_force = total_force / count
            output = f'average impact force: {average_force}'
    except (FileNotFoundError, ValueError):
        output = 'No data available'
    with open(output_filename, 'w') as output_file:
        output_file.write(output)