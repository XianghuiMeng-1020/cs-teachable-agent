def calculate_final_weight(filename):
    with open(filename, 'r') as file:
        changes = file.readlines()
    initial_weight = 1000
    final_weight = initial_weight + sum(int(change.strip()) for change in changes)
    with open('final_weight.txt', 'w') as output_file:
        output_file.write(f'{final_weight}')