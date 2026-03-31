def calculate_power(filename):
    with open(filename, 'r') as file:
        power_changes = file.readline().strip().split(',')
    total_change = sum(int(change) for change in power_changes)
    final_power_level = 1000 + total_change
    return final_power_level