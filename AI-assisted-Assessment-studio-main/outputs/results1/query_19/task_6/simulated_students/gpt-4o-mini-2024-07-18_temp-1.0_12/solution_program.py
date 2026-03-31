import os

def analyze_asteroid_reports(input_filename, output_filename):
    if not os.path.exists(input_filename):
        with open(output_filename, 'w') as output_file:
            output_file.write("No data available")
        return

    total_force = 0
    count = 0
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if line.strip():
                parts = line.split(',')
                if len(parts) == 2:
                    try:
                        impact_force = float(parts[1].strip())
                        total_force += impact_force
                        count += 1
                    except ValueError:
                        continue

    if count == 0:
        with open(output_filename, 'w') as output_file:
            output_file.write("No data available")
    else:
        average_force = total_force / count
        with open(output_filename, 'w') as output_file:
            output_file.write(f"average impact force: {average_force}")