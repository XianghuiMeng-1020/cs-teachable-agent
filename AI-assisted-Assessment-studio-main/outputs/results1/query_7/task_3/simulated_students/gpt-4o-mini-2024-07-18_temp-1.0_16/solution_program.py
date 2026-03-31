def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as infile:
        creatures = infile.readlines()
    filtered_creatures = []
    for creature in creatures:
        name, legend_status = creature.strip().split(':')
        if legend_status == status:
            filtered_creatures.append(name)
    with open(output_filename, 'w') as outfile:
        for name in filtered_creatures:
            outfile.write(name + '\n')