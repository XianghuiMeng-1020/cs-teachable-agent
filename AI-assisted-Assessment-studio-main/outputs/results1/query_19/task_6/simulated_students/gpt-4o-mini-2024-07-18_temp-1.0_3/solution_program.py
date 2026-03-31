def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                raise ValueError('No data available')
            total_force = 0
            count = 0
            for line in lines:
                asteroid_id, impact_force = line.strip().split(',')
                total_force += float(impact_force)
                count += 1
            average_force = total_force / count
            result = f'average impact force: {average_force}'
    except (FileNotFoundError, ValueError) as e:
        result = 'No data available'

    with open(output_filename, 'w') as output_file:
        output_file.write(result)