def compute_mythical_stats(filename):
    creatures = []
    total_power = 0
    highest_power = 0
    highest_creature = None

    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    name, power = line.rsplit(' ', 1)
                    power = int(power)
                    creatures.append((name, power))
                    total_power += power
                    if power > highest_power:
                        highest_power = power
                        highest_creature = name
    except FileNotFoundError:
        creatures = []

    total_creatures = len(creatures)

    # Calculate average power level
    if total_creatures > 0:
        average_power = total_power / total_creatures
    else:
        average_power = 0.00
        highest_creature = 'None'

    with open('stats.txt', 'w') as stats_file:
        stats_file.write(f'{average_power:.2f}\n')
        stats_file.write(f'{highest_creature}\n')
        stats_file.write(f'{total_creatures}\n')