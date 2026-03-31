def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return

    if not lines:
        average_power = 0.00
        highest_creature = 'None'
        total_creatures = 0
    else:
        total_power = 0
        highest_power = -1
        highest_creature = ''
        total_creatures = 0

        for line in lines:
            if line.strip():
                total_creatures += 1
                name, power_str = line.split()
                power = int(power_str)
                total_power += power
                if power > highest_power:
                    highest_power = power
                    highest_creature = name

        average_power = total_power / total_creatures if total_creatures > 0 else 0.00

    with open('stats.txt', 'w') as stats_file:
        stats_file.write(f'{average_power:.2f}\n')
        stats_file.write(f'{highest_creature}\n')
        stats_file.write(f'{total_creatures}\n')
