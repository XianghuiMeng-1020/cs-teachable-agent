def calculate_final_weight(filename):
    total_weight = 1000
    with open(filename, 'r') as file:
        for line in file:
            total_weight += int(line.strip())
    with open('final_weight.txt', 'w') as output_file:
        output_file.write(f'{total_weight}')