def calculate_power(filename):
    with open(filename, 'r') as file:
        changes = file.read().strip().split(',')
    total_change = sum(int(change) for change in changes)
    initial_power_level = 1000
    final_power_level = initial_power_level + total_change
    return final_power_level