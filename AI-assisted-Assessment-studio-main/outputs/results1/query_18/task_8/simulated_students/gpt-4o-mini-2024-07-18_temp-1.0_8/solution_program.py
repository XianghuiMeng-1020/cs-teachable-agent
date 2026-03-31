def generate_energy_report(input_file, output_file):
    total_energy = 0
    units_count = 0
    try:
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    unit_id, energy = line.split(',')
                    total_energy += float(energy)
                    units_count += 1
    except FileNotFoundError:
        print(f"{input_file} not found.")
        return
    except ValueError:
        print(f"Error processing the file. Check the format.")
        return

    average_energy = total_energy / units_count if units_count > 0 else 0

    with open(output_file, 'w') as f:
        f.write(f"Total Energy: {total_energy} kWh\n")
        f.write(f"Average Energy: {average_energy:.2f} kWh\n")
