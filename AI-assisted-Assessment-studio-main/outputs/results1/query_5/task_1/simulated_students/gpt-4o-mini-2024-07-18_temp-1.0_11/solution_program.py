def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if not lines:
            with open('stats.txt', 'w') as stats_file:
                stats_file.write('0.00\nNone\n0\n')
            return

        total_power = 0
        highest_power = -1
        highest_creature = None
        creature_count = 0

        for line in lines:
            if line.strip():
                creature, power = line.split()
                power = int(power)
                total_power += power
                creature_count += 1
                if power > highest_power:
                    highest_power = power
                    highest_creature = creature

        average_power = total_power / creature_count if creature_count else 0
        with open('stats.txt', 'w') as stats_file:
            stats_file.write(f'{average_power:.2f}\n')
            stats_file.write(f'{highest_creature if highest_creature else "None"}\n')
            stats_file.write(f'{creature_count}\n')
    except FileNotFoundError:
        with open('stats.txt', 'w') as stats_file:
            stats_file.write('0.00\nNone\n0\n')
    except Exception as e:
        print(f'An error occurred: {e}' )