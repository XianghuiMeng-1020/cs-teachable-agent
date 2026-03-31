def analyze_pantheon():
    try:
        with open('pantheon.txt', 'r') as file:
            gods = []
            for line in file:
                name, power = line.strip().split(',')
                gods.append((name, int(power)))

        if not gods:
            return None

        min_god = max_god = gods[0]
        total_power = min_power = max_power = gods[0][1]

        for god in gods[1:]:
            name, power = god
            total_power += power
            
            if power < min_power:
                min_god = god
                min_power = power
            if power > max_power:
                max_god = god
                max_power = power

        average_power = total_power // len(gods)

        return (min_god[0], max_god[0], average_power)
    except IOError:
        return None