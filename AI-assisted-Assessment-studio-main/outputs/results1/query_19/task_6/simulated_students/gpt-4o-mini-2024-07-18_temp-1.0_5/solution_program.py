def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile:
            lines = infile.readlines()
            if not lines:
                raise ValueError('No data available')
            total_force = 0
            count = 0
            for line in lines:
                asteroid_id, impact_force = line.strip().split(',')
                total_force += float(impact_force)
                count += 1
            average_force = total_force / count if count > 0 else 0
            with open(output_filename, 'w') as outfile:
                outfile.write(f'average impact force: {average_force}\n')
    except FileNotFoundError:
        with open(output_filename, 'w') as outfile:
            outfile.write('No data available\n')
    except ValueError as e:
        with open(output_filename, 'w') as outfile:
            outfile.write('No data available\n')