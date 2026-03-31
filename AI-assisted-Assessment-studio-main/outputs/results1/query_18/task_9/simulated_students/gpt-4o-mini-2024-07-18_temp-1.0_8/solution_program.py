def calculate_total_consumption(input_file, output_file):
    total_consumption = 0
    with open(input_file, 'r') as infile:
        for line in infile:
            planet, consumption = line.split()
            total_consumption += int(consumption)
    with open(output_file, 'w') as outfile:
        outfile.write(str(total_consumption))