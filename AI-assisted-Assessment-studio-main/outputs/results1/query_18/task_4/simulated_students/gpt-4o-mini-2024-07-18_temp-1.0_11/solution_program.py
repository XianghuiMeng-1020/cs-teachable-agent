def calculate_power(filename):
    with open(filename, 'r') as file:
        changes = file.readline().strip().split(',')
        changes = map(int, changes)
        final_power = 1000 + sum(changes)
    return final_power