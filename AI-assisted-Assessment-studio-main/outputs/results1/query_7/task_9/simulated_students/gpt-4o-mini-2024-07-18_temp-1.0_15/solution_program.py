def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    processed_lines = []
    for line in lines:
        # Strip whitespace and split the line at the first hyphen
        parts = line.strip().split('-', 1)
        if len(parts) == 2:
            title = parts[0].strip()
            description = parts[1].strip()

            # Reverse words and convert to uppercase
            reversed_title = ' '.join(reversed(title.split())).upper()
            reversed_description = ' '.join(reversed(description.split())).upper()

            # Prepare the processed line
            processed_line = f'{reversed_title} - {reversed_description}'
            processed_lines.append(processed_line)

    with open(output_file, 'w') as outfile:
        for processed_line in processed_lines:
            outfile.write(processed_line + '\n')