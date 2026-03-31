def generate_energy_report(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        total_energy = 0
        num_units = 0
        
        for line in lines:
            if line.strip():  # Ensure the line is not empty
                unit, energy = line.split(",")
                total_energy += float(energy)
                num_units += 1

        if num_units == 0:  # Avoid division by zero
            average_energy = 0.0
        else:
            average_energy = total_energy / num_units

        with open(output_file, 'w') as report:
            report.write(f"Total Energy: {total_energy} kWh\n")
            report.write(f"Average Energy: {average_energy:.2f} kWh\n")

    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function for testing
if __name__ == "__main__":
    generate_energy_report('energy_data.txt', 'energy_report.txt')