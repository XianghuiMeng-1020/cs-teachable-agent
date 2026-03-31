def compute_mythical_stats(filename):
    try:
        with open(filename, 'r') as file:
            creatures = file.readlines()
    except FileNotFoundError:
        creatures = []

    if not creatures:
        stats = ["0.00", "None", "0"]
    else:
        total_power = 0
        highest_power = 0
        highest_creature = ""
        count = 0

        for line in creatures:
            parts = line.split()
            name = parts[0]
            power = int(parts[1])
            total_power += power
            count += 1

            if power > highest_power:
                highest_power = power
                highest_creature = name

        average_power = total_power / count
        stats = [f"{average_power:.2f}", highest_creature, str(count)]

    with open('stats.txt', 'w') as outfile:
        for stat in stats:
            outfile.write(stat + '\n')

