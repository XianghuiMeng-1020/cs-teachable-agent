def calculate_final_weight(filename):
    with open(filename, 'r') as file:
        weight_changes = file.readlines()

    final_weight = 1000  
    for change in weight_changes:
        final_weight += int(change.strip())

    with open('final_weight.txt', 'w') as output_file:
        output_file.write(str(final_weight))