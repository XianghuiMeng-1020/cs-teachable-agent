def calculate_final_weight(filename):
    with open(filename, 'r') as file:
        changes = file.readlines()

    final_weight = 1000
    for change in changes:
        final_weight += int(change.strip())

    with open('final_weight.txt', 'w') as output_file:
        output_file.write(f'{final_weight}')