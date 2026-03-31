def calculate_final_weight(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    final_weight = 1000
    for line in lines:
        final_weight += int(line.strip())
    with open('final_weight.txt', 'w') as output_file:
        output_file.write(str(final_weight))