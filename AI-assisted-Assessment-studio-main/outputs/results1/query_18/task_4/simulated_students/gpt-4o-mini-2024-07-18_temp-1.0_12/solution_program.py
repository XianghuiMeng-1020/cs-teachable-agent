def calculate_power(filename):
    with open(filename, 'r') as file:
        changes = file.readline().strip().split(',')
        changes = [int(change) for change in changes]
    initial_power = 1000
    final_power = initial_power + sum(changes)
    return final_power