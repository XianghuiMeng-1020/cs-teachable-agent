def calculate_power(filename):
    with open(filename, 'r') as file:
        changes = file.readline().strip().split(',')
        total_power_change = sum(int(change) for change in changes)
        final_power_level = 1000 + total_power_change
        return final_power_level