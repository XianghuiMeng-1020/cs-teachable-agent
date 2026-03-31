def calculate_total_consumption(input_file, output_file):
    total_consumption = 0
    with open(input_file, 'r') as file:
        for line in file:
            _, consumption = line.split()
            total_consumption += int(consumption)
    with open(output_file, 'w') as file:
        file.write(str(total_consumption))