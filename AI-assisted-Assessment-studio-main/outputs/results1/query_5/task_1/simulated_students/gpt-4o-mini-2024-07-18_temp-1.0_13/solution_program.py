def compute_mythical_stats(filename):
    creatures = []
    total_power = 0
    highest_power = float('-inf')
    highest_creature = None
    total_creatures = 0

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                name = parts[0]
                try:
                    power = int(parts[1])
                    creatures.append((name, power))
                    total_power += power
                    total_creatures += 1
                    if power > highest_power:
                        highest_power = power
                        highest_creature = name
                except ValueError:
                    continue

    if total_creatures == 0:
        average_power = 0.00
        highest_creature = 'None'
    else:
        average_power = total_power / total_creatures

    with open('stats.txt', 'w') as output_file:
        output_file.write(f'{average_power:.2f}\n')
        output_file.write(f'{highest_creature}\n')
        output_file.write(f'{total_creatures}\n')