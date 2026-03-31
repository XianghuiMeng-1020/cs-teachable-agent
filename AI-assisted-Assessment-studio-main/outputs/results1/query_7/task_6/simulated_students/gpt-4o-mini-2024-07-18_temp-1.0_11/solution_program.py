def filter_mythical_creatures(input_file, output_file, origin):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    filtered_lines = [line for line in lines if line.startswith(origin)]
    with open(output_file, 'w') as outfile:
        outfile.writelines(filtered_lines)