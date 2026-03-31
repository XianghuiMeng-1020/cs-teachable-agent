def compute_mythical_stats(filename):
    creature_list = []
    total_power = 0
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                name, power = line.split()
                power = int(power)
                creature_list.append((name, power))
                total_power += power
    
    if creature_list:
        average_power = total_power / len(creature_list)
        average_power_formatted = format(average_power, ".2f")
        max_creature = max(creature_list, key=lambda x: x[1])[0]
        total_creatures = len(creature_list)
    else:
        average_power_formatted = "0.00"
        max_creature = "None"
        total_creatures = 0
    
    with open('stats.txt', 'w') as file:
        file.write(f"{average_power_formatted}\n{max_creature}\n{total_creatures}\n")
