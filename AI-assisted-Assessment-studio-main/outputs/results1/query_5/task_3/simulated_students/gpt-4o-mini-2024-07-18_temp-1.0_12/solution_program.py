def analyze_pantheon():
    try:
        with open('pantheon.txt', 'r') as file:
            lines = file.readlines()
    except IOError:
        return None

    min_name = None
    max_name = None
    min_power = float('inf')
    max_power = float('-inf')
    total_power = 0
    count = 0

    for line in lines:
        name, power = line.strip().split(', ')
        power = int(power)
        total_power += power
        count += 1

        if power < min_power:
            min_power = power
            min_name = name
        if power > max_power:
            max_power = power
            max_name = name

    average_power = total_power // count

    return (min_name, max_name, average_power)