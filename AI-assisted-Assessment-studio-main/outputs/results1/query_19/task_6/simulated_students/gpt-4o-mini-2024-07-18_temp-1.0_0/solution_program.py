def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                raise ValueError('No data available')
            total_force = 0
            count = 0
            for line in lines:
                try:
                    asteroid_id, impact_force = line.strip().split(',')
                    total_force += float(impact_force)
                    count += 1
                except ValueError:
                    continue
            if count == 0:
                with open(output_filename, 'w') as out_file:
                    out_file.write('No data available')
                return
            average_force = total_force / count
            with open(output_filename, 'w') as out_file:
                out_file.write(f'average impact force: {average_force}')
    except FileNotFoundError:
        with open(output_filename, 'w') as out_file:
            out_file.write('No data available')