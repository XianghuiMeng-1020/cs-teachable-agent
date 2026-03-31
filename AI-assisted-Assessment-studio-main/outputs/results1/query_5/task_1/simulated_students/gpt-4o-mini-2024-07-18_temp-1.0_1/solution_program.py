def compute_mythical_stats(filename):
    creatures = []
    total_power = 0
    highest_power = 0
    highest_creature = None

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                name, power = line.split()
                power = int(power)
                creatures.append((name, power))
                total_power += power
                if power > highest_power:
                    highest_power = power
                    highest_creature = name

    num_creatures = len(creatures)

    if num_creatures == 0:
        average_power = 0.00
        highest_creature = 'None'
    else:
        average_power = total_power / num_creatures

    with open('stats.txt', 'w') as stats_file:
        stats_file.write(f'{average_power:.2f}\n')
        stats_file.write(f'{highest_creature}\n')
        stats_file.write(f'{num_creatures}\n')