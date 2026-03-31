def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile:
            lines = infile.readlines()

        if not lines:
            average_impact_force = "No data available"
        else:
            total_force = 0
            total_count = 0
            for line in lines:
                asteroid_data = line.strip().split(',')
                if len(asteroid_data) == 2:
                    impact_force = float(asteroid_data[1])
                    total_force += impact_force
                    total_count += 1

            if total_count > 0:
                average_impact_force = total_force / total_count
            else:
                average_impact_force = "No data available"

    except FileNotFoundError:
        average_impact_force = "No data available"
    except Exception as e:
        average_impact_force = "No data available"

    with open(output_filename, 'w') as outfile:
        outfile.write(f"average impact force: {average_impact_force}")
