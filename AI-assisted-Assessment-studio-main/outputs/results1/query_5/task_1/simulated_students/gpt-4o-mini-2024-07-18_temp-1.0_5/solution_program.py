def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if not lines:
            average_power = 0.00
            highest_power_creature = 'None'
            total_creatures = 0
        else:
            total_power = 0
            highest_power = 0
            highest_power_creature = ''
            total_creatures = len(lines)

            for line in lines:
                if line.strip():
                    name, power = line.split()
                    power = int(power)
                    total_power += power
                    if power > highest_power:
                        highest_power = power
                        highest_power_creature = name

            average_power = total_power / total_creatures

        with open('stats.txt', 'w') as output_file:
            output_file.write(f'{average_power:.2f}\n')
            output_file.write(f'{highest_power_creature}\n')
            output_file.write(f'{total_creatures}\n')
    except Exception as e:
        with open('stats.txt', 'w') as output_file:
            output_file.write('0.00\nNone\n0\n')
