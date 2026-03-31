def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as file:
            total_force = 0
            count = 0
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    asteroid_id, impact_force = parts
                    total_force += float(impact_force)
                    count += 1

            if count > 0:
                average_force = total_force / count
                result = f'average impact force: {average_force}'
            else:
                result = 'No data available'
    except FileNotFoundError:
        result = 'No data available'
    except Exception as e:
        result = f'Error: {str(e)}'

    with open(output_filename, 'w') as output_file:
        output_file.write(result)
