def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    total_power = 0
    max_power = 0
    max_creature = None
    creature_count = 0

    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            creature_name = parts[0]
            try:
                power_level = int(parts[1])
                total_power += power_level
                creature_count += 1
                if power_level > max_power:
                    max_power = power_level
                    max_creature = creature_name
            except ValueError:
                continue

    if creature_count == 0:
        average_power = 0.00
        max_creature = "None"
    else:
        average_power = total_power / creature_count

    with open('stats.txt', 'w') as stats_file:
        stats_file.write(f'{average_power:.2f}\n')
        stats_file.write(f'{max_creature}\n')
        stats_file.write(f'{creature_count}\n')

compute_mythical_stats('creatures.txt')