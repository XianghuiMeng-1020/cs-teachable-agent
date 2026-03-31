def calculate_power(filename):
    initial_power = 1000
    with open(filename, 'r') as file:
        content = file.read().strip()
        if content:
            changes = map(int, content.split(','))
            for change in changes:
                initial_power += change
    return initial_power
