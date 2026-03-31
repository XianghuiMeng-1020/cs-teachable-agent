def calculate_power(filename):
    with open(filename, 'r') as file:
        line = file.readline().strip()
        changes = map(int, line.split(','))
        final_power = 1000 + sum(changes)
    return final_power