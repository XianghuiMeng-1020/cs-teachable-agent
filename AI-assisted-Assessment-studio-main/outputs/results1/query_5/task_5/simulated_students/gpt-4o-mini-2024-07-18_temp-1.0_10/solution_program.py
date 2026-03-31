def identify_legendary_creatures(input_file, output_file):
    with open(input_file, 'r') as infile:
        creatures = infile.readlines()

    legendary_creatures = []
    for creature in creatures:
        parts = creature.split()
        name = parts[0]
        power = int(parts[1])
        skill = int(parts[2])
        if power >= 90 and skill >= 75:
            legendary_creatures.append(name)

    with open(output_file, 'w') as outfile:
        for name in legendary_creatures:
            outfile.write(name + '\n')