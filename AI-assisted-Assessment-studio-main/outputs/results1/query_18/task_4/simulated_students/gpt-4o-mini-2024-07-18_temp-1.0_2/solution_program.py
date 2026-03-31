def calculate_power(filename):
    with open(filename, 'r') as file:
        power_changes = file.readline().strip().split(',')
    final_power = 1000
    for change in power_changes:
        final_power += int(change)
    return final_power