def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    if not lines:
        avg_power = 0.00
        highest_creature = 'None'
        total_creatures = 0
    else:
        total_power = 0
        max_power = -1
        highest_creature = ''
        total_creatures = len(lines)

        for line in lines:
            name, power_str = line.strip().split()
            power = int(power_str)
            total_power += power
            if power > max_power:
                max_power = power
                highest_creature = name

        avg_power = total_power / total_creatures

    with open('stats.txt', 'w') as stats_file:
        stats_file.write(f'{avg_power:.2f}\n')
        stats_file.write(f'{highest_creature}\n')
        stats_file.write(f'{total_creatures}\n')