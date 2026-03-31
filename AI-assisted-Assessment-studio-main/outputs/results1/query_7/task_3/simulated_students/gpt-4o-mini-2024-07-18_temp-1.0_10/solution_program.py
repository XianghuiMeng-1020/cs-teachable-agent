def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
    filtered_creatures = []
    for line in lines:
        creature, legendary_status = line.strip().split(':')
        if legendary_status == status:
            filtered_creatures.append(creature)
    with open(output_filename, 'w') as outfile:
        for creature in filtered_creatures:
            outfile.write(creature + '\n')