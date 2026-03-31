def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                raise ValueError('No data available')

            total_force = 0
            count = 0

            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    try:
                        impact_force = float(parts[1])
                        total_force += impact_force
                        count += 1
                    except ValueError:
                        continue

            if count == 0:
                average_force = 'No data available'
            else:
                average_force = total_force / count
                average_force = f'average impact force: {average_force}'

    except FileNotFoundError:
        average_force = 'No data available'

    with open(output_filename, 'w') as output_file:
        output_file.write(str(average_force))