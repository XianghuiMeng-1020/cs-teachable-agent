def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as infile:
        creatures = infile.readlines()

    filtered_creatures = [line.split(':')[0] for line in creatures if line.strip().endswith(status)]

    with open(output_filename, 'w') as outfile:
        for creature in filtered_creatures:
            outfile.write(creature + '\n')