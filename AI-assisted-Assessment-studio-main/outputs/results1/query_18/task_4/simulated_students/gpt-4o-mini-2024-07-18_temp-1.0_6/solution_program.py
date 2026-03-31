def calculate_power(filename):
    with open(filename, 'r') as file:
        changes = file.readline().strip().split(',')
        total_change = sum(int(change.strip()) for change in changes)
    return 1000 + total_change