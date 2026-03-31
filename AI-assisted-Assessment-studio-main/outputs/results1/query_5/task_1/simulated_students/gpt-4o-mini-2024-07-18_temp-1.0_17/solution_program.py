def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []
    
    if not lines:
        average_power = 0.00
        strongest_creature = 'None'
        total_creatures = 0
    else:
        total_power = 0
        max_power = -1
        strongest_creature = ''
        total_creatures = len(lines)
        
        for line in lines:
            name, power = line.rsplit(' ', 1)
            power = int(power)
            total_power += power
            if power > max_power:
                max_power = power
                strongest_creature = name

        average_power = total_power / total_creatures

    average_power = round(average_power, 2)
    with open('stats.txt', 'w') as stat_file:
        stat_file.write(f'{average_power}\n')
        stat_file.write(f'{strongest_creature}\n')
        stat_file.write(f'{total_creatures}\n')