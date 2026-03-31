def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if not lines:
            avg_power = 0.00
            highest_creature = 'None'
            total_creatures = 0
        else:
            total_power = 0
            highest_power = float('-inf')
            highest_creature = ''
            total_creatures = 0

            for line in lines:
                parts = line.split()
                creature_name = parts[0]
                power_level = int(parts[1])

                total_power += power_level
                total_creatures += 1

                if power_level > highest_power:
                    highest_power = power_level
                    highest_creature = creature_name

            avg_power = total_power / total_creatures

        with open('stats.txt', 'w') as output_file:
            output_file.write(f'{avg_power:.2f}\n')
            output_file.write(f'{highest_creature}\n')
            output_file.write(f'{total_creatures}\n')
    except FileNotFoundError:
        avg_power = 0.00
        highest_creature = 'None'
        total_creatures = 0
        with open('stats.txt', 'w') as output_file:
            output_file.write(f'{avg_power:.2f}\n')
            output_file.write(f'{highest_creature}\n')
            output_file.write(f'{total_creatures}\n')
    except Exception as e:
        print(f'An error occurred: {e}'}