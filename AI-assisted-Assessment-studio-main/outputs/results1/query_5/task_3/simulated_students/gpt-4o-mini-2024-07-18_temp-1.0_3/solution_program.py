def analyze_pantheon():
    try:
        with open('pantheon.txt', 'r') as file:
            lines = file.readlines()

        gods = []
        total_power = 0

        for line in lines:
            name, power = line.strip().split(',')
            power = int(power)
            gods.append((name, power))
            total_power += power

        min_god = min(gods, key=lambda x: x[1])
        max_god = max(gods, key=lambda x: x[1])
        average_power = total_power // len(gods)

        return (min_god[0], max_god[0], average_power)
    except IOError:
        return ('Error reading file', 'Error reading file', 0)