def identify_legendary_creatures(input_file, output_file):
    with open(input_file, 'r') as infile:
        legendary_creatures = []
        for line in infile:
            parts = line.split()
            name = parts[0]
            power = int(parts[1])
            skill = int(parts[2])
            if power >= 90 and skill >= 75:
                legendary_creatures.append(name)

    with open(output_file, 'w') as outfile:
        for creature in legendary_creatures:
            outfile.write(creature + '\n')