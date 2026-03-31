def calculate_final_weight(filename):
    initial_weight = 1000
    final_weight = initial_weight
    with open(filename, 'r') as file:
        for line in file:
            weight_change = int(line.strip())
            final_weight += weight_change
    with open('final_weight.txt', 'w') as output_file:
        output_file.write(str(final_weight))