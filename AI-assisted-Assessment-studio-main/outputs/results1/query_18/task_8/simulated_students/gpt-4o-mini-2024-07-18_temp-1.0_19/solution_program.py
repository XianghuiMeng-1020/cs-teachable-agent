def generate_energy_report(input_file, output_file):
    total_energy = 0
    unit_count = 0

    with open(input_file, 'r') as file:
        for line in file:
            if line.strip():
                unit_id, energy = line.split(',')
                total_energy += float(energy)
                unit_count += 1

    average_energy = 0
    if unit_count > 0:
        average_energy = total_energy / unit_count

    with open(output_file, 'w') as report:
        report.write(f'Total Energy: {total_energy} kWh\n')
        report.write(f'Average Energy: {average_energy:.2f} kWh')