def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return

    if not lines:
        with open('stats.txt', 'w') as stats_file:
            stats_file.write('0.00\nNone\n0')
        return

    total_power = 0
    max_power = -1
    max_creature = None
    creature_count = 0

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        creature = parts[0]
        try:
            power = int(parts[1])
        except ValueError:
            continue

        total_power += power
        creature_count += 1
        if power > max_power:
            max_power = power
            max_creature = creature

    average_power = total_power / creature_count if creature_count > 0 else 0
    average_power = round(average_power, 2)

    with open('stats.txt', 'w') as stats_file:
        stats_file.write(f'{average_power:.2f}\n')
        stats_file.write(f'{max_creature if max_creature else "None"}\n')
        stats_file.write(f'{creature_count}\n')