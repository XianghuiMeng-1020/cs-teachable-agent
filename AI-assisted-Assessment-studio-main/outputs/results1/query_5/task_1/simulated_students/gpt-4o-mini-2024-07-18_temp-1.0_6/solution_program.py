def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    if not lines:
        with open('stats.txt', 'w') as output:
            output.write('0.00\nNone\n0')
        return

    total_power = 0
    creature_count = 0
    highest_power = -1
    highest_creature = None

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        creature = parts[0]
        power = int(parts[1])
        total_power += power
        creature_count += 1

        if power > highest_power:
            highest_power = power
            highest_creature = creature

    average_power = total_power / creature_count if creature_count > 0 else 0
    average_power_str = f'{average_power:.2f}'
    highest_creature_str = highest_creature if highest_creature is not None else 'None'

    with open('stats.txt', 'w') as output:
        output.write(f'{average_power_str}\n')
        output.write(f'{highest_creature_str}\n')
        output.write(f'{creature_count}\n')