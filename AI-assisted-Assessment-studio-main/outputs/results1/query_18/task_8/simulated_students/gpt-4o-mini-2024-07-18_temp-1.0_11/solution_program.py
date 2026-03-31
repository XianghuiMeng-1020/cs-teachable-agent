def generate_energy_report(input_file, output_file):
    total_energy = 0
    units_count = 0
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                unit_id, energy_consumed = line.strip().split(',')
                total_energy += float(energy_consumed)
                units_count += 1
    except FileNotFoundError:
        return
    except ValueError:
        return
    average_energy = total_energy / units_count if units_count > 0 else 0
    with open(output_file, 'w') as f:
        f.write(f'Total Energy: {total_energy} kWh\n')
        f.write(f'Average Energy: {average_energy:.2f} kWh\n')