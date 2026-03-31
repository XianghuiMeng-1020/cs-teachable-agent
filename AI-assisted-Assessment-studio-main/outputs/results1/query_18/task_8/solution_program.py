def generate_energy_report(input_file, output_file):
    total_energy = 0
    unit_count = 0
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                _, energy = line.split(',')
                total_energy += float(energy)
                unit_count += 1
    average_energy = total_energy / unit_count if unit_count > 0 else 0
    with open(output_file, 'w') as file:
        file.write(f"Total Energy: {int(total_energy)} kWh\n")
        file.write(f"Average Energy: {average_energy:.2f} kWh\n")
