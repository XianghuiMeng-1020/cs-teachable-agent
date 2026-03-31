def compute_mythical_stats(filename):
    creatures = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    name, power = line.split() 
                    creatures.append((name, int(power)))
    except FileNotFoundError:
        creatures = []

    total_creatures = len(creatures)
    if total_creatures == 0:
        average_power = 0.00
        highest_power_creature = None
    else:
        total_power = sum(power for _, power in creatures)
        average_power = total_power / total_creatures
        highest_power_creature = max(creatures, key=lambda x: x[1])[0]

    with open('stats.txt', 'w') as f:
        f.write(f'{average_power:.2f}\n')
        f.write(f'{highest_power_creature}\n')
        f.write(f'{total_creatures}\n')
