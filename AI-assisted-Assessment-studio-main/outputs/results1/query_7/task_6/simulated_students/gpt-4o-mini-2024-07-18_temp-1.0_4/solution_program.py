def filter_mythical_creatures(input_file, output_file, origin):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    filtered_lines = []
    for line in lines:
        parts = line.strip().split(':')
        if len(parts) >= 4 and parts[1] == origin:
            filtered_lines.append(line.strip())

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(filtered_lines) + '\n')