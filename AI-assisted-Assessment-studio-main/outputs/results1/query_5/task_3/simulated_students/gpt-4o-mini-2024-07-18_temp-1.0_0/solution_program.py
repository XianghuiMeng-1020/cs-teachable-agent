def analyze_pantheon():
    try:
        with open('pantheon.txt', 'r') as file:
            gods = []
            total_power = 0
            for line in file:
                name, power = line.strip().split(', ')
                power = int(power)
                gods.append((name, power))
                total_power += power

            if not gods:
                return None

            min_god = min(gods, key=lambda x: x[1])
            max_god = max(gods, key=lambda x: x[1])
            average_power = total_power // len(gods)

            return (min_god[0], max_god[0], average_power)
    except Exception as e:
        print(f'An error occurred: {e}')