def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
    filtered_creatures = [line.split(':')[0] for line in lines if line.strip().endswith(status)]
    with open(output_filename, 'w') as outfile:
        outfile.write('\n'.join(filtered_creatures) + '\n')