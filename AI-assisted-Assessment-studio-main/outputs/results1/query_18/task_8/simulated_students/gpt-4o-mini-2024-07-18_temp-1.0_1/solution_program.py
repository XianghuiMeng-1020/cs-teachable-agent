def generate_energy_report(input_file, output_file):
    total_energy = 0
    unit_count = 0
    try:
        with open(input_file, 'r') as file:
            for line in file:
                if line.strip():
                    unit_id, energy = line.split(',')
                    total_energy += float(energy)
                    unit_count += 1
    except FileNotFoundError:
        print(f"The file {input_file} does not exist.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if unit_count > 0:
        average_energy = total_energy / unit_count
    else:
        average_energy = 0

    with open(output_file, 'w') as report:
        report.write(f'Total Energy: {total_energy} kWh\n')
        report.write(f'Average Energy: {average_energy:.2f} kWh\n')
