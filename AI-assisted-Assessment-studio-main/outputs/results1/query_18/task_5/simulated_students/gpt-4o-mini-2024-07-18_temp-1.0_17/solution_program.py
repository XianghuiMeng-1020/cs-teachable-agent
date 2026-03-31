def calculate_final_weight(filename):
    with open(filename, 'r') as file:
        weight_changes = [int(line.strip()) for line in file.readlines()]

    initial_weight = 1000
    final_weight = initial_weight + sum(weight_changes)

    with open('final_weight.txt', 'w') as output_file:
        output_file.write(str(final_weight))