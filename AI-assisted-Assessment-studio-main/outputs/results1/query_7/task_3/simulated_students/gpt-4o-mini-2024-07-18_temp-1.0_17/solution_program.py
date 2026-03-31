def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as input_file:
        creatures = input_file.readlines()
    filtered_creatures = []
    for creature in creatures:
        name, creature_status = creature.strip().split(':')
        if creature_status == status:
            filtered_creatures.append(name)
    with open(output_filename, 'w') as output_file:
        for name in filtered_creatures:
            output_file.write(name + '\n')