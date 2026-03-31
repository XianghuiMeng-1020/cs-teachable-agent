def identify_legendary_creatures(input_file, output_file):
    with open(input_file, 'r') as infile:
        creatures = infile.readlines()

    legendary_creatures = []
    for creature in creatures:
        name, power, skill = creature.split()
        power = int(power)
        skill = int(skill)
        if power >= 90 and skill >= 75:
            legendary_creatures.append(name)

    with open(output_file, 'w') as outfile:
        for legendary in legendary_creatures:
            outfile.write(legendary + '\n')