def calculate_power(filename):
    with open(filename, 'r') as file:
        changes = file.readline().strip().split(',')
    initial_power_level = 1000
    total_change = sum(int(change.strip()) for change in changes)
    final_power_level = initial_power_level + total_change
    return final_power_level