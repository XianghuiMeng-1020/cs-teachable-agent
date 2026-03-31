def calculate_power(filename):
    with open(filename, 'r') as file:
        power_changes = file.readline().strip().split(',')
        total_power_change = sum(int(change) for change in power_changes)
        initial_power_level = 1000
        final_power_level = initial_power_level + total_power_change
    return final_power_level