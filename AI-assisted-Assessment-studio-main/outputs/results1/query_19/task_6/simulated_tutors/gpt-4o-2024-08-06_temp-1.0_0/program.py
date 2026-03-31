def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile:
            lines = infile.readlines()
            if not lines or all(line.strip() == "" for line in lines):
                with open(output_filename, 'w') as outfile:
                    outfile.write("No data available")
                return

            total_impact_force = 0
            count = 0
            for line in lines:
                line = line.strip()
                if not line:  # handle empty lines
                    continue
                try:
                    _, impact_force = line.split(",")
                    total_impact_force += float(impact_force)
                    count += 1
                except ValueError:
                    pass  # in case of malformed line, we skip

            if count == 0:
                with open(output_filename, 'w') as outfile:
                    outfile.write("No data available")
            else:
                average_impact_force = total_impact_force / count
                with open(output_filename, 'w') as outfile:
                    outfile.write(f"average impact force: {average_impact_force:.2f}")

    except FileNotFoundError:
        with open(output_filename, 'w') as outfile:
            outfile.write("No data available")