def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as infile:
        creatures = infile.readlines()
        filtered_creatures = [line.split(':')[0] for line in creatures if line.split(':')[1].strip() == status]
    with open(output_filename, 'w') as outfile:
        outfile.write('\n'.join(filtered_creatures))
