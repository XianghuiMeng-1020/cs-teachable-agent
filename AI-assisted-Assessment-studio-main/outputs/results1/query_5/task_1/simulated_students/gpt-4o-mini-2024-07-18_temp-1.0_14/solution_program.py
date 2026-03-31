def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return

    total_power = 0
    creature_count = 0
    highest_power = -1
    creature_with_highest_power = None

    for line in lines:
        if line.strip():
            creature_count += 1
            name, power = line.split()
            power = int(power)
            total_power += power
            if power > highest_power:
                highest_power = power
                creature_with_highest_power = name

    if creature_count == 0:
        average_power = 0.00
        creature_with_highest_power = None
    else:
        average_power = round(total_power / creature_count, 2)

    with open('stats.txt', 'w') as output_file:
        output_file.write(f'{average_power:.2f}\n')
        output_file.write(f'{creature_with_highest_power if creature_with_highest_power else "None"}\n')
        output_file.write(f'{creature_count}\n'}