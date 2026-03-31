def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                result = "No data available"
            else:
                total_force = 0
                count = 0
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) != 2:
                        continue  # skip lines that are not correctly formatted
                    try:
                        impact_force = float(parts[1])
                        total_force += impact_force
                        count += 1
                    except ValueError:
                        continue  # skip lines where impact_force cannot be converted to float
                if count == 0:
                    result = "No data available"
                else:
                    average_force = total_force / count
                    result = f"average impact force: {average_force}"
    except FileNotFoundError:
        result = "No data available"

    with open(output_filename, 'w') as output_file:
        output_file.write(result)