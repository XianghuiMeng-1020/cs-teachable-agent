def compute_mythical_stats(filename):
    creatures = []
    total_power = 0
    max_power = -1
    max_creature = None
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    name, power = line.split()  
                    power = int(power)
                    creatures.append((name, power))
                    total_power += power
                    if power > max_power:
                        max_power = power
                        max_creature = name
    except FileNotFoundError:
        pass

    total_creatures = len(creatures)

    if total_creatures == 0:
        average_power = 0.00
        max_creature = None
    else:
        average_power = total_power / total_creatures

    with open('stats.txt', 'w') as stats_file:
        stats_file.write(f'{average_power:.2f}\n')
        stats_file.write(f'{max_creature if max_creature else "None"}\n')
        stats_file.write(f'{total_creatures}\n'}