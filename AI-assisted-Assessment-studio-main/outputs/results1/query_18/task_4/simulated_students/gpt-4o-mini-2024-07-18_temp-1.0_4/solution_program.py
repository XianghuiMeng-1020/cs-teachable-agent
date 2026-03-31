def calculate_power(filename):
    with open(filename, 'r') as file:
        changes = file.read().strip().split(',')
    initial_power = 1000
    total_change = sum(int(change) for change in changes)
    final_power = initial_power + total_change
    return final_power