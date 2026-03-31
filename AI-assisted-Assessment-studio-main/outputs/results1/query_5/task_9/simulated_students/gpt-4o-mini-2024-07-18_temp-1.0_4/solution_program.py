def determine_ultimate_being(input_file_path):
    creatures = []
    with open(input_file_path, 'r') as file:
        for line in file:
            name, power = line.strip().split(';')
            creatures.append((name, int(power)))

    max_power = -1
    ultimate_creatures = []

    for creature in creatures:
        name, power = creature
        if power > max_power:
            max_power = power
            ultimate_creatures = [name]
        elif power == max_power:
            ultimate_creatures.append(name)

    result = "It's a draw" if len(ultimate_creatures) > 1 else ultimate_creatures[0]

    with open('ultimate_being.txt', 'w') as output_file:
        output_file.write(result)