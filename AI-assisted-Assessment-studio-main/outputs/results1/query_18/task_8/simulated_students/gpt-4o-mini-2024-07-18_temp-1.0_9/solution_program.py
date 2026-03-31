def generate_energy_report(input_file, output_file):
    total_energy = 0
    unit_count = 0

    try:
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    unit_data = line.split(',')
                    if len(unit_data) == 2:
                        unit_id, energy = unit_data[0], unit_data[1]
                        try:
                            energy_consumed = float(energy)
                            total_energy += energy_consumed
                            unit_count += 1
                        except ValueError:
                            continue
    except FileNotFoundError:
        return

    average_energy = total_energy / unit_count if unit_count > 0 else 0

    with open(output_file, 'w') as f:
        f.write(f'Total Energy: {total_energy} kWh\n')
        f.write(f'Average Energy: {average_energy:.2f} kWh\n')