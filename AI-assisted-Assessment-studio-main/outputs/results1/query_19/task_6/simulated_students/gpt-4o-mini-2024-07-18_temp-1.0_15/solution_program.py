def analyze_asteroid_reports(input_filename, output_filename):
    import os
    if not os.path.exists(input_filename):
        with open(output_filename, 'w') as f:
            f.write("No data available")
        return
    total_force = 0
    count = 0
    with open(input_filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                asteroid_id, impact_force = line.strip().split(',')
                total_force += float(impact_force)
                count += 1
            except ValueError:
                continue
    if count == 0:
        with open(output_filename, 'w') as f:
            f.write("No data available")
    else:
        average_force = total_force / count
        with open(output_filename, 'w') as f:
            f.write(f"average impact force: {average_force}")