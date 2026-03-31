def identify_legendary_creatures(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    legendary_creatures = []
    for line in lines:
        parts = line.split()
        name = parts[0]
        power = int(parts[1])
        skill = int(parts[2])
        if power >= 90 and skill >= 75:
            legendary_creatures.append(name)
    with open(output_file, 'w') as f:
        for creature in legendary_creatures:
            f.write(creature + '\n')