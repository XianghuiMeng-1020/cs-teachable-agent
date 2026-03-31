def generate_energy_report(input_file, output_file):
    total_energy = 0.0
    unit_count = 0
    try:
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.split(',')
                    if len(parts) == 2:
                        try:
                            energy = float(parts[1])
                            total_energy += energy
                            unit_count += 1
                        except ValueError:
                            continue
    except FileNotFoundError:
        return

    average_energy = total_energy / unit_count if unit_count > 0 else 0.0

    with open(output_file, 'w') as f:
        f.write(f'Total Energy: {total_energy} kWh\n')
        f.write(f'Average Energy: {average_energy:.2f} kWh\n')