def analyze_pantheon():
    try:
        with open('pantheon.txt', 'r') as f:
            gods = f.readlines()
    except IOError:
        return None
    min_power = float('inf')
    max_power = -float('inf')
    total_power = 0
    count = 0
    min_name = ''
    max_name = ''
    for line in gods:
        name, power_str = line.split(',')
        power = int(power_str)
        if power < min_power:
            min_power = power
            min_name = name
        if power > max_power:
            max_power = power
            max_name = name
        total_power += power
        count += 1
    average_power = total_power // count
    return min_name, max_name, average_power