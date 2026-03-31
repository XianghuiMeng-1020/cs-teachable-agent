def calculate_final_weight(filename):
    final_weight = 1000
    with open(filename, 'r') as file:
        for line in file:
            final_weight += int(line.strip())
    with open('final_weight.txt', 'w') as output_file:
        output_file.write(str(final_weight))