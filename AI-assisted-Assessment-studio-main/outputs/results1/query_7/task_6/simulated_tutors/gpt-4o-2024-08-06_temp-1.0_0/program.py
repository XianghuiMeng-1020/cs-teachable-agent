def filter_mythical_creatures(input_file, output_file, origin):
    # Open the input file and read lines
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    # Prepare a list for filtered lines
    filtered_lines = []
    
    # Process each line to filter by origin
    for line in lines:
        parts = line.strip().split(':')
        if len(parts) >= 2 and parts[1] == origin:
            filtered_lines.append(line.strip())

    # Write the filtered result to the output file
    with open(output_file, 'w') as outfile:
        for filtered_line in filtered_lines:
            outfile.write(filtered_line + "\n")