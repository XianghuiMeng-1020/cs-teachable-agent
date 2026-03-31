def calculate_power(filename):
    with open(filename, 'r') as file:
        changes = file.readline().strip().split(',')
    total_change = sum(int(change) for change in changes)
    final_power_level = 1000 + total_change
    return final_power_level