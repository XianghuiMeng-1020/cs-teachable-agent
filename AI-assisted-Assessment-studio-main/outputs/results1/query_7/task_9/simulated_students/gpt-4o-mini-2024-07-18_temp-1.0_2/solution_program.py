def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    processed_lines = []
    for line in lines:
        title, description = line.split('-', 1)
        title = title.strip()
        description = description.strip()

        reversed_title = ' '.join(reversed(title.upper().split()))
        reversed_description = ' '.join(reversed(description.upper().split()))

        processed_lines.append(f'{reversed_title} - {reversed_description}')

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(processed_lines) + '\n')