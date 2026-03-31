def analyze_asteroid_reports(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as file:
            lines = file.readlines()

        total_force = 0
        count = 0

        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(',')
                try:
                    force = float(parts[1])
                    total_force += force
                    count += 1
                except (IndexError, ValueError):
                    continue

        if count == 0:
            result = "No data available"
        else:
            average = total_force / count
            result = "average impact force: {:.2f}".format(average)

    except FileNotFoundError:
        result = "No data available"

    with open(output_filename, 'w') as out_file:
        out_file.write(result)