def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as infile:
        creatures = infile.readlines()
    filtered_creatures = [creature.split(':')[0] for creature in creatures if creature.split(':')[1].strip() == status]
    with open(output_filename, 'w') as outfile:
        for creature in filtered_creatures:
            outfile.write(creature + '\n')