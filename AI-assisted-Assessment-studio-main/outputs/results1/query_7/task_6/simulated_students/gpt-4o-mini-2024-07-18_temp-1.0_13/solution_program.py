def filter_mythical_creatures(input_file, output_file, origin):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.strip():
                parts = line.strip().split(':')
                if len(parts) == 4 and parts[1] == origin:
                    outfile.write(line)