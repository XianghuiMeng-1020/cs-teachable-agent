def generate_energy_report(input_file, output_file):
    total_energy = 0
    unit_count = 0

    try:
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    unit_id, energy_str = line.split(',')
                    energy = float(energy_str)
                    total_energy += energy
                    unit_count += 1
    except (FileNotFoundError, ValueError):
        pass

    if unit_count > 0:
        average_energy = total_energy / unit_count
    else:
        average_energy = 0

    with open(output_file, 'w') as report:
        report.write(f'Total Energy: {total_energy} kWh\n')
        report.write(f'Average Energy: {average_energy:.2f} kWh\n')
