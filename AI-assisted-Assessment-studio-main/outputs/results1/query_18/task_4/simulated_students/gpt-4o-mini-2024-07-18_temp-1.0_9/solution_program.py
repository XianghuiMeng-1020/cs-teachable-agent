def calculate_power(filename):
    with open(filename, 'r') as file:
        changes = file.readline().strip().split(',')
        power_level = 1000
        for change in changes:
            power_level += int(change)
    return power_level