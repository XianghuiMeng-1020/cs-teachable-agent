def analyze_pantheon():
    try:
        with open('pantheon.txt', 'r') as file:
            lines = file.readlines()
    except IOError:
        return 'Error reading the file.'

    gods = []
    total_power = 0
    for line in lines:
        name, power = line.strip().split(',')
        power = int(power)
        gods.append((name, power))
        total_power += power

    min_name = gods[0][0]
    min_power = gods[0][1]
    max_name = gods[0][0]
    max_power = gods[0][1]

    for name, power in gods:
        if power < min_power:
            min_power = power
            min_name = name
        if power > max_power:
            max_power = power
            max_name = name

    average_power = total_power // len(gods)
    return (min_name, max_name, average_power)