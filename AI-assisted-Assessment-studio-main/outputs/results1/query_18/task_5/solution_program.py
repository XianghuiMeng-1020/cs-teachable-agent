def calculate_final_weight(filename):
    with open(filename, 'r') as file:
        modifications = file.readlines()
    current_weight = 1000
    for modification in modifications:
        change = int(modification.strip())
        current_weight += change
    with open('final_weight.txt', 'w') as result_file:
        result_file.write(f"{current_weight}\n")