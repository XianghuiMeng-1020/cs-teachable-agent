def process_mythology_data(input_file, output_file):
    # Open the input file for reading
    with open(input_file, 'r') as file:
        lines = file.readlines()

    processed_lines = []

    # Process each line
    for line in lines:
        # Split the line into title and description
        parts = line.split('-', 1)
        if len(parts) == 2:
            title, description = parts
        else:
            title, description = parts[0], ''

        # Strip white spaces
        title = title.strip()
        description = description.strip()

        # Reverse words in title and description, convert to uppercase
        title_reversed = ' '.join(title.split()[::-1]).upper()
        description_reversed = ' '.join(description.split()[::-1]).upper()

        # Combine back the elements
        processed_line = f'{title_reversed} - {description_reversed}'
        processed_lines.append(processed_line)

    # Write the processed data to the output file
    with open(output_file, 'w') as file:
        for processed_line in processed_lines:
            file.write(processed_line + '\n')