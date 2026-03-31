def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile:
            lines = infile.readlines()
            total_force = 0
            count = 0

            for line in lines:
                if line.strip():
                    asteroid_id, impact_force = line.split(',')
                    total_force += float(impact_force)
                    count += 1

            if count == 0:
                average_force = 'No data available'
            else:
                average_force = total_force / count
                average_force = f'average impact force: {average_force}'

    except FileNotFoundError:
        average_force = 'No data available'
        
    with open(output_filename, 'w') as outfile:
        outfile.write(str(average_force))