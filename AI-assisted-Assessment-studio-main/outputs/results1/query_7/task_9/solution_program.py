def process_mythology_data(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    processed_lines = []
    for line in lines:
        parts = line.split('-', 1)
        if len(parts) > 1:
            title, description = parts
        else:
            title, description = parts[0].strip(), ''
        reversed_title = ' '.join(reversed(title.strip().upper().split()))
        reversed_description = ' '.join(reversed(description.strip().upper().split()))
        processed_line = f"{reversed_title} - {reversed_description}"
        processed_lines.append(processed_line)
    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(processed_lines))