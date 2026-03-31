def analyze_pantheon():
    try:
        with open('pantheon.txt', 'r') as file:
            data = file.readlines()
    except IOError:
        return None

    gods = []
    for line in data:
        name, power = line.strip().split(', ')
        gods.append((name, int(power)))

    if not gods:
        return None

    min_god = min(gods, key=lambda x: x[1])
    max_god = max(gods, key=lambda x: x[1])
    average_power = sum(power for _, power in gods) // len(gods)

    return (min_god[0], max_god[0], average_power)