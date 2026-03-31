def determine_ultimate_being(input_file_path):
    creatures = {}
    with open(input_file_path, 'r') as file:
        for line in file:
            name, power = line.strip().split(';')
            creatures[name] = int(power)

    max_power = max(creatures.values())
    ultimate_creatures = [name for name, power in creatures.items() if power == max_power]

    result = ultimate_creatures[0] if len(ultimate_creatures) == 1 else "It's a draw"

    with open('ultimate_being.txt', 'w') as outfile:
        outfile.write(result)