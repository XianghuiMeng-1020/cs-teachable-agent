def generate_energy_report(input_file, output_file):
    total_energy = 0
    unit_count = 0

    try:
        with open(input_file, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    unit_id, energy = parts[0], parts[1]
                    try:
                        energy_consumed = float(energy)
                        total_energy += energy_consumed
                        unit_count += 1
                    except ValueError:
                        continue
    except FileNotFoundError:
        return

    average_energy = total_energy / unit_count if unit_count > 0 else 0

    with open(output_file, 'w') as report_file:
        report_file.write(f'Total Energy: {total_energy} kWh\n')
        report_file.write(f'Average Energy: {average_energy:.2f} kWh\n')