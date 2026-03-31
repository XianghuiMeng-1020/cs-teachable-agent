def determine_ultimate_being(input_file_path):
    creatures = {}
    with open(input_file_path, 'r') as infile:
        for line in infile:
            name, power = line.strip().split(';')
            creatures[name] = int(power)

    max_power = max(creatures.values())
    ultimate_creatures = [name for name, power in creatures.items() if power == max_power]

    result = "It's a draw" if len(ultimate_creatures) > 1 else ultimate_creatures[0]

    with open('ultimate_being.txt', 'w') as outfile:
        outfile.write(result)