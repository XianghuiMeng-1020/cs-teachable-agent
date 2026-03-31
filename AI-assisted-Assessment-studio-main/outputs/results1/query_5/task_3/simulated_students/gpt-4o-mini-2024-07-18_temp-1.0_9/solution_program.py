def analyze_pantheon():
    try:
        with open('pantheon.txt', 'r') as file:
            lines = file.readlines()

        gods = []
        for line in lines:
            name, power = line.strip().split(',')
            gods.append((name, int(power)))

        min_god = min(gods, key=lambda x: x[1])
        max_god = max(gods, key=lambda x: x[1])

        total_power = sum(power for _, power in gods)
        average_power = total_power // len(gods)

        return (min_god[0], max_god[0], average_power)
    except Exception as e:
        print(f'Error occurred: {e}')