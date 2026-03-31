def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as file:
        lines = file.readlines()
    filtered_creatures = []
    for line in lines:
        creature, creature_status = line.strip().split(':')
        if creature_status == status:
            filtered_creatures.append(creature)
    with open(output_filename, 'w') as file:
        for creature in filtered_creatures:
            file.write(creature + '\n')