def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            creatures = []
            power_levels = []
            for line in file:
                line = line.strip()
                if line:
                    name, power = line.rsplit(' ', 1)
                    power = int(power)
                    creatures.append(name)
                    power_levels.append(power)
        if not power_levels:
            avg_power = 0.00
            max_creature = None
            total_creatures = 0
        else:
            avg_power = sum(power_levels) / len(power_levels)
            max_power = max(power_levels)
            max_creature = creatures[power_levels.index(max_power)]
            total_creatures = len(creatures)
    except FileNotFoundError:
        avg_power = 0.00
        max_creature = None
        total_creatures = 0

    with open('stats.txt', 'w') as stats_file:
        stats_file.write(f'{avg_power:.2f}\n')
        stats_file.write(f'{max_creature}\n')
        stats_file.write(f'{total_creatures}\n')