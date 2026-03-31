def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile:
            lines = infile.readlines()
            if not lines:
                output = "No data available"
            else:
                total_force = 0
                count = 0
                for line in lines:
                    data = line.strip().split(',')
                    if len(data) == 2:
                        asteroid_id, impact_force = data
                        total_force += float(impact_force)
                        count += 1
                if count == 0:
                    output = "No data available"
                else:
                    average_force = total_force / count
                    output = f"average impact force: {average_force}"
    except FileNotFoundError:
        output = "No data available"
    with open(output_filename, 'w') as outfile:
        outfile.write(output)