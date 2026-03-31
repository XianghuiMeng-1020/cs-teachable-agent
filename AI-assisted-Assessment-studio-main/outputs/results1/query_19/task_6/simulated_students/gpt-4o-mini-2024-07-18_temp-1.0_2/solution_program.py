def analyze_asteroid_reports(input_filename, output_filename):
    import os
    if not os.path.exists(input_filename):
        with open(output_filename, 'w') as out_file:
            out_file.write('No data available')
        return
    with open(input_filename, 'r') as in_file:
        lines = in_file.readlines()
    if not lines:
        with open(output_filename, 'w') as out_file:
            out_file.write('No data available')
        return
    total_impact_force = 0
    count = 0
    for line in lines:
        try:
            parts = line.strip().split(',')
            impact_force = float(parts[1])
            total_impact_force += impact_force
            count += 1
        except (IndexError, ValueError):
            continue
    if count == 0:
        with open(output_filename, 'w') as out_file:
            out_file.write('No data available')
    else:
        average_impact_force = total_impact_force / count
        with open(output_filename, 'w') as out_file:
            out_file.write(f'average impact force: {average_impact_force}')